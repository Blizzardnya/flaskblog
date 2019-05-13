from flask import Flask, render_template, url_for

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
