# import libraries and dependencies
from flask import Flask, render_template, redirect, url_for, flash, session, request
from forms import LoginForm, RegistrationForm, NotesForm, UpdateNotesForm
from flask_wtf import CSRFProtect
from flask_session import Session
from cs50 import SQL

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# connect to the database
db = SQL("sqlite:///_instance/notes.db")

# Configure a secret key 
app.config['SECRET_KEY'] = 'this_is_a_secret_key'

csrf = CSRFProtect(app)
# Index route for the home page
@app.route('/')
def index():
    title = 'Home'
    return render_template('index.html', title=title)

# Login route
@app.route('/login',  methods=['POST', 'GET'])
def login():
    title = 'Login'
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # get data from the users table
        user = db.execute("SELECT username, password FROM users WHERE username = ?", username)
        if user:
            user = user[0]
            session['username'] = user['username'] # let the username be stored into the session container
            if user['username'] == username and user['password'] == password:
                return redirect(url_for('home'))
            flash("Wrong username or password")
        flash("Wrong username or password")
    return render_template('login.html', title=title, form=form)

# Registration route
@app.route("/register", methods=['POST', 'GET'])
def register():

    title='Register'
    form = RegistrationForm()

    if form.validate_on_submit():

        users = db.execute('SELECT * FROM users')
        username = form.username.data
        email = form.email.data
        password = form.password.data

        for user in users:
            if username == user['username'] or email == user['email']:
                flash("User already exist!")
                return redirect(url_for('register'))
            
        db.execute("INSERT INTO users(username, email, password) VALUES (?, ?, ?)", username, email, password)
        flash("Registered successfully!")
        return redirect('login')
    return render_template('register.html', form=form, title=title)

# home page where users will be taking notes
@app.route('/home', methods=['POST', 'GET'])
def home():
    user_id = db.execute("SELECT id FROM users WHERE username = (?)", (session.get("username")))
    if user_id:
        user_id = user_id[0]['id']
    count = db.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", user_id)
    count = count[0]['COUNT(*)']

    notes = db.execute("SELECT notes.id, notes.content, category.name, notes.title FROM notes JOIN users ON users.id = notes.user_id JOIN category ON category.id = notes.category_id WHERE notes.user_id = ? ORDER BY notes.created_at DESC", user_id)

    return render_template('home.html', username=session.get("username"), notes=notes, count=count)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Add route
@app.route('/add', methods=["POST", "GET"])
def add():
    form = NotesForm()
    category = form.category.data

    category_id = db.execute("SELECT id FROM category WHERE name = (?)", category)
    if category_id:
        category_id = category_id[0]['id']

    user_id = db.execute("SELECT id FROM users WHERE username = (?)", (session.get("username")))
    if user_id:
        user_id = user_id[0]['id']
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        db.execute("INSERT INTO notes(user_id, title, content, category_id) VALUES(?, ?, ?, ?)", user_id, title, content, category_id)

        flash("Note added successfully!")
        return redirect(url_for("home"))
    return render_template('add.html', username=session.get("username"), form=form)

# Delete notes route
@app.route('/notes/<int:note_id>')
def notes(note_id):
    db.execute("DELETE FROM notes WHERE id = (?)", note_id)
    flash("Note deleted!")
    return redirect(url_for('home'))

# Read  route
@app.route('/read/<int:note_id>')
def read(note_id):
    note = db.execute("SELECT notes.id, notes.title, notes.content, category.name, notes.created_at FROM notes JOIN category ON category.id = notes.category_id WHERE notes.id = (?)", note_id)
    note = note[0]
    return render_template("read.html", note=note)
    
# Edit route
@app.route('/edit/<int:note_id>', methods=['POST', 'GET'])
def edit(note_id):
    form=UpdateNotesForm()
    # get the note content to be displayed to be edited
    note = db.execute("SELECT notes.id, notes.title, notes.content, category.name FROM notes JOIN category ON category.id = notes.category_id WHERE notes.id = (?)", note_id)
    if note:
        note = note[0]
    if request.method == 'GET':
        form.update_category.data = note['name'] 
        form.update_title.data = note['title']
        form.update_content.data = note['content']

    # Update the note
    category = form.update_category.data
    category_id = db.execute("SELECT id FROM category WHERE name = (?)", category)
    if category_id:
        category_id = category_id[0]['id']

    user_id = db.execute("SELECT id FROM users WHERE username = (?)", (session.get("username")))
    if user_id:
        user_id = user_id[0]['id']
    
    if form.validate_on_submit():
        update_title = form.update_title.data
        update_content = form.update_content.data
        print(update_title)
        print(update_content)

        db.execute("UPDATE notes SET user_id = ?, title = ?, content = ?, category_id = ? WHERE id = ?", (user_id), (update_title), (update_content), (category_id), (note_id))


        flash("Note updated successfully!")
        return redirect(url_for("home"))
    return render_template("edit.html", note=note, form=form)
    

if __name__ == "__main__":
    app.run(debug=True)