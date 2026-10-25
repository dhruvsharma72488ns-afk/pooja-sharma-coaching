from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = 'pooja_sharma_coaching_secret_key_fixed'

DB_FILE = 'users.json'

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))

        users = load_users()

        if username in users:
            flash('This username is already registered!', 'danger')
            return redirect(url_for('register'))

        # Save username and direct plain password to JSON database permanently
        users[username] = password
        save_users(users)

        flash('Account created successfully! You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        users = load_users()

        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password! Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()

        users = load_users()

        if username in users:
            user_password = users[username]
            return render_template('forgot.html', recovered_password=user_password, username=username)
        else:
            flash('This username is not registered!', 'danger')
            return redirect(url_for('forgot'))

    return render_template('forgot.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)