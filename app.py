from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --------------------- Models ---------------------

class passwordsaver(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    website = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<passwordsaver {self.sno}>"

class notessaver(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100))
    content = db.Column(db.Text)
    date = db.Column(db.Date)

# --------------------- Password Saver Routes ---------------------

@app.route('/')
def index():
    allsavepassword = passwordsaver.query.all()
    return render_template('index.html', allsavepassword=allsavepassword)

@app.route('/', methods=['POST'])
def register():
    website = request.form["website"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_website = passwordsaver(
        website=website,
        email=email,
        username=username,
        password=hashed_password
    )
    db.session.add(new_website)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:sno>', methods=['GET'])
def delete(sno):
    delete_savepassword = passwordsaver.query.get(sno)
    if delete_savepassword:
        db.session.delete(delete_savepassword)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:sno>', methods=['GET'])
def update_form(sno):
    update_savepassword = passwordsaver.query.get(sno)
    if update_savepassword:
        return render_template('update.html', data=update_savepassword)
    return redirect(url_for('index'))

@app.route('/update/<int:sno>', methods=['POST'])
def update(sno):
    update_savepassword = passwordsaver.query.get(sno)
    if update_savepassword:
        update_savepassword.email = request.form["email"]
        update_savepassword.username = request.form["username"]
        new_password = request.form["password"]
        update_savepassword.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
    return redirect(url_for('index'))

# --------------------- Notes Routes ---------------------

@app.route('/note', methods=["GET", "POST"])
def notes():
    notes = notessaver.query.all()
    return render_template("notes.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    topic = request.form["topic"]
    content = request.form["content"]
    date_str = request.form["date"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    new_note = notessaver(topic=topic, content=content, date=date_obj)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for("notes"))

@app.route("/notes/delete/<int:sno>")
def delete_note(sno):
    notes_delete = notessaver.query.get(sno)
    if notes_delete:
        db.session.delete(notes_delete)
        db.session.commit()
    return redirect(url_for("notes"))

@app.route("/notes/update/<int:sno>")
def update_note(sno):
    notes_update = notessaver.query.get(sno)
    if notes_update:
        return render_template("update_notes.html", data=notes_update)
    return redirect(url_for("notes"))

@app.route('/notes/update/<int:sno>', methods=['POST'])
def update_note_sno(sno):
    notes_update = notessaver.query.get(sno)
    if notes_update:
        notes_update.topic = request.form["topic"]
        notes_update.content = request.form["content"]
        date_str = request.form["date"]
        notes_update.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        db.session.commit()
    return redirect(url_for('notes'))

# --------------------- Run the App ---------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
