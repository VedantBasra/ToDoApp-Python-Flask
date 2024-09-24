from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy # type: ignore


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    todo_list= Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    #add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    #update the state 
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #delete item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

# Route to handle editing a task
@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()

    if request.method == "POST":
        new_title = request.form.get("title")
        todo.title = new_title
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit.html", todo=todo)

@app.route('/about')
def about():
    return "About"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
