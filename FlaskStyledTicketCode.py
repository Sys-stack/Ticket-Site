from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'

# Database configuration for Render using PostgreSQL
# You can use 'sqlite:///tickets.db' for local development
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tickets.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # New field for admin check

# Ticket Model
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("User registered successfully! Please log in.")
        return redirect(url_for('login'))
    return render_template('https://raw.githubusercontent.com/Sys-stack/Ticket-Site/refs/heads/CSS/html/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check username and password.')
    return render_template('https://raw.githubusercontent.com/Sys-stack/Ticket-Site/refs/heads/CSS/html/login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user_tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('https://raw.githubusercontent.com/Sys-stack/Ticket-Site/refs/heads/CSS/html/dashboard.html', tickets=user_tickets)

@app.route('/add_ticket', methods=['GET', 'POST'])
@login_required
def add_ticket():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_ticket = Ticket(title=title, description=description, user_id=current_user.id)
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_ticket.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Admin route to view all tickets
@app.route('/admin/tickets')
@login_required
def view_all_tickets():
    if not current_user.is_admin:
        flash("You do not have permission to access this page.")
        return redirect(url_for('dashboard'))
    
    all_tickets = Ticket.query.all()  # Fetch all tickets
    return render_template('https://raw.githubusercontent.com/Sys-stack/Ticket-Site/refs/heads/CSS/html/sdmin_tickets.html', tickets=all_tickets)

# Temporary admin creation (only for initial testing)
@app.route('/make_admin/<username>')
@login_required
def make_admin(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user.is_admin = True
        db.session.commit()
        flash(f"{username} is now an admin.")
    else:
        flash("User not found.")
    return redirect(url_for('dashboard'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
