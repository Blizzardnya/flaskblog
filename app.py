from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a1781f7ff39d1aeda34f9780b71aa59f'

posts = [
    {
        'author': 'BlizzardNya',
        'title': 'About snikers',
        'content': 'This snikers is awesome',
        'date_posted': 'May 13, 2019'
    },
    {
        'author': 'Sorokin',
        'title': 'About snikers 2',
        'content': 'Test dummy data',
        'date_posted': 'May 12, 2019'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Accounts created for {0}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'pass':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
