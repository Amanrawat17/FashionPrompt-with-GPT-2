# FashionGen Text Generation App
This repository contains a Flask web application that uses a fine-tuned GPT-2 model to generate text based on descriptions from the FashionGen dataset. The application enables users to log in, enter prompts, and receive relevant generated text. It also includes user registration and authentication features.

Features
Text Generation: Generate text based on FashionGen descriptions using a fine-tuned GPT-2 model.
User Authentication: Register, log in, and log out functionality using Flask-Login.
Database: User data is stored in an SQLite database.
Preprocessing: Data from the FashionGen dataset is preprocessed and split for model training.
Model Fine-Tuning: Code to fine-tune GPT-2 on the FashionGen dataset.
Flask App: Simple web interface to generate text based on user prompts.
# Clone the repository
```` 
git clone https://github.com/Amanrawat17/FashionPrompt-with-GPT-2.git
```` 
![diagram-export-10-29-2024-3_22_39-PM](https://github.com/user-attachments/assets/13bd0bce-90f8-4696-8619-dc1a48325ac4)

# Navigate into the project directory
cd FashionPrompt-with-GPT-2
````
# Create a virtual environment named "website"
python -m venv website
```` 
# Activate the virtual environment
# For Windows
website\Scripts\activate
# For MacOS/Linux
source website/bin/activate
````
# Install necessary packages
pip install -r requirements.txt
```` 
# Run the application
python app.py


![diagram-export-10-29-2024-3_08_41-PM](https://github.com/user-attachments/assets/8a445ab6-1800-4bd1-b648-fd5d834559b6)
