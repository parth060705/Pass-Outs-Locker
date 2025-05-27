from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" # to create database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)

# -------------------------------------------------------------------------------------------
# define the model
class passwordsaver(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    website = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<passwordsaver {self.sno}>" # for print the specific data
# --------------------------------------------------------------------------------------------

@app.route('/')    
def index():
    allsavepassword=passwordsaver.query.all()
    return render_template('index.html', allsavepassword=allsavepassword) # to render template file

# to post the credential to database
@app.route('/', methods=['POST'])
def register():
    website = request.form["website"]
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]
    
    new_website = passwordsaver(website=website, email=email, username=username, password=password)
    db.session.add(new_website) # to add the data 
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:sno>', methods=['GET'])
def delete(sno):
    delete_savepassword = passwordsaver.query.filter_by(sno=sno).first()
    if delete_savepassword:
        db.session.delete(delete_savepassword) # to delete the data
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:sno>', methods=['GET'])
def update_form(sno):
    update_savepassword = passwordsaver.query.filter_by(sno=sno).first()
    if update_savepassword:
        return render_template('update.html', data = update_savepassword) # to render template file and switch to the update page
    return redirect(url_for('index'))

@app.route('/update/<int:sno>', methods=['POST'])# update the credentials
def update(sno):
    update_savepassword = passwordsaver.query.filter_by(sno=sno).first()
    if update_savepassword:
        update_savepassword.email = request.form["email"]
        update_savepassword.username = request.form["username"]
        update_savepassword.password = request.form["password"]
        db.session.commit()
    return redirect(url_for('index'))

# =======================2 Model================
class notessaver(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String(100))
    content = db.Column(db.Text)

@app.route('/note', methods=["GET","POST"])    
def notes():
    notes = notessaver.query.all()
    return render_template("notes.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    # sno = request.form["sno"]
    topic = request.form["topic"]
    content = request.form["content"]

    new_note = notessaver(topic=topic, content=content)
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



# to start the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)