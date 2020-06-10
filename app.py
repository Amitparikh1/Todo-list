## Imports
from flask import Flask, render_template,url_for,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

## Set up database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']  ## Get form content
        new_task = Todo(content=task_content) 
        try: ## add to database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)
## Delete 
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) #get the id or throw a 404 error
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') # redirect to homepage
    except:
        return 'There was a problem deleting that task'
## Update
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html',task=task)
## if app.py is run directly
if __name__ == "__main__":
    app.run(debug=True) 