import git
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/seoproject2/seo12')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '09caa9c3ed2e73dcc19673eb7d14b8d3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

with app.app_context():
    db.create_all()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/second_page")
def second_page():
    return render_template('second_page.html', subtitle='This is Eshaals & Pavels about me page', text='')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
