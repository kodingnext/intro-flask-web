from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Application definition
app = Flask(__name__, 
    static_url_path='/static', 
    static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'


# Database definition
db = SQLAlchemy(app)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)

db.create_all()


# Route definition
@app.route('/', methods=['GET'])
def list_todo_item():
    todo_items = TodoItem.query.all()
    return render_template('todo_list.html', todo_items=todo_items)


@app.route('/create', methods=['POST'])
def create_todo_item():
    item_desc = request.form['description']
    todo_item = TodoItem(description=item_desc)
    try:
        db.session.add(todo_item)
        db.session.commit()
        return redirect(url_for('list_todo_item'))
    except Exception:
        return 'Failed to add todo item'


@app.route('/modify/<todo_item_id>', methods=['GET'])
def modify_todo_item(todo_item_id):
    todo_item = TodoItem.query.filter_by(id=todo_item_id)
    todo_item = todo_item.first()

    if todo_item is None:
        return f'Todo Item #{todo_item_id} is not exists'

    return render_template('todo_modify.html', todo_item=todo_item)


@app.route('/update/<todo_item_id>', methods=['POST'])
def update_todo_item(todo_item_id):
    item_desc = request.form['description']

    todo_item = TodoItem.query.filter_by(id=todo_item_id)
    todo_item = todo_item.first()

    if todo_item is None:
        return f'Todo Item #{todo_item_id} is not exists'

    try:
        todo_item.description = item_desc
        db.session.commit()
        return redirect(url_for('list_todo_item'))
    except Exception:
        return f'Failed to update todo item #{todo_item.id}'


@app.route('/delete/<todo_item_id>', methods=['GET'])
def delete_todo_item(todo_item_id):
    todo_item = TodoItem.query.filter_by(id=todo_item_id)
    todo_item = todo_item.first()

    if todo_item is None:
        return f'Todo item #{todo_item_id} is not exists'
    
    try:
        db.session.delete(todo_item)
        db.session.commit()
        return redirect(url_for('list_todo_item'))
    except Exception:
        return 'Failed to delete todo item'


# Run the application
if __name__ == '__main__':
    app.run(debug=True)