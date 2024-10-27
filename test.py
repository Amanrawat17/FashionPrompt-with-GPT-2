import os
import pickle
import gdown
import torch
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User

app = Flask(__name__)

# Set the secret key for session management
app.secret_key = 'xn\xa6<\x00p\x12b\xf6\x0e\xf1\n\xc0\xdc\xe1\r\xc8\xf0\x08r\xe7GtU'  # Replace with a random secret key

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: to suppress a warning

# Initialize the SQLAlchemy object with the app
db.init_app(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create database
with app.app_context():
    db.create_all()  # This creates the database tables

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def download_model():
    # File ID from your Google Drive link
    file_id = '1_c4MLmBi7CDafQYZ8b7uQaHd6zAsAuHs'
    output_path = 'fin_tuned_gpt2.pkl'
    
    # Download the model from Google Drive
    gdown.download(f'https://drive.google.com/uc?id={file_id}', output_path, quiet=False)
    
    # Load the model and tokenizer from the .pkl file
    with open(output_path, 'rb') as f:
        model, tokenizer = pickle.load(f)
    
    return model, tokenizer

# Download the model and tokenizer at the start
model, tokenizer = download_model()

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to the login page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        # Hash the password using pbkdf2:sha256
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')  # Render the text generation interface on the dashboard

# Define a function to generate text
def generate_text(prompt, max_length=20000):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        num_return_sequences=1,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    prompt = request.form['prompt']
    generated_text = generate_text(prompt)
    return render_template('index.html', prompt=prompt, generated_text=generated_text)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
