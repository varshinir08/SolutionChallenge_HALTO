from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='/static')

app.secret_key = 'your_secret_key'

# For simplicity, we are using a dictionary as an in-memory store
users = {'admin': generate_password_hash('admin')}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and check_password_hash(users[username], password):
        session['username'] = username
        return redirect(url_for('homepage'))
    # return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid username or password')

@app.route('/homepage')
def homepage():
    if 'username' in session:
        return render_template('homepage.html', username=session['username'])
    else:
        return redirect(url_for('index'))
    
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')

    #     return render_template('dashboard.html', username=session['username'])
    # else:
    #     return redirect(url_for('index'))
@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            users[username] = generate_password_hash(password)
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', error='Username already exists')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
