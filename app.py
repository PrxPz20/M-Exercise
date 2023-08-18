from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 
app.app_context().push()

 
#  Create database
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable = False )
    completed = db.Column(db.Boolean, nullable = False, default=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Main home page
@app.route('/')
def index():
    allTodo = Task.query.all()
    return render_template('index.html', allTodo=allTodo)


# Adding new task to the database 
@app.route('/database', methods=['POST'])
def add_task():

    data = request.form

    if request.form.get("Status") != None:
        new_task = Task(title=data['Title'], description=data['Description'], completed= True)
    else:
        new_task = Task(title=data['Title'], description=data['Description'], completed=False)

    try:
        db.session.add(new_task)
        db.session.commit()
        allTodo = Task.query.all()
        return redirect('/')

    except Exception as e:
        return "Error"


# Deleting task from database
@app.route('/delete/<int:id>')
def delete_task(id):

    task_id_delete = Task.query.get_or_404(id)

    try:
        db.session.delete(task_id_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Invalid ID, please return to the Main page"


# Updating a task from database
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):  

    todo = Task.query.get_or_404(id)
    data = request.form

    if request.method == 'POST':
        todo.title = data['Title']
        todo.description = data['Description']
        
        if request.form.get("Status") != None:
            todo.completed = True
        else:
            todo.completed = False
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Error"

    else:
        return render_template('update.html', todo=todo)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
