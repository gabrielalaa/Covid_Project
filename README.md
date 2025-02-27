# Covid Project

## About the project

As a **student researcher**, I was tasked with exploring various tools for machine learning, multilingual support, and data privacy. Throughout my learning journey, I experimented with:

- **Multilingual Support:** Google Translate API and Django i18n 
- **AI Integration:** scikit-learn, TensorFlow, and PyTorch
- **Data Privacy:** PyCryptodome and Django ORM

After testing these tools individually, I decided to build **Covid_Project**, which combines multiple technologies in a **Django-based web application**.

---

## Features 

### **Home Page**
- Displays **COVID-19 evolution** and **vaccination progress** in Romania.
- Allows users to switch between **English** and **Romanian** using **Django i18n**.
- Although i18n worked well, writing translations manually was a bit tedious.

### **Account Creation & Encryption**
- Users can **create an account** with a **username, password, and message**.
- The **message is encrypted** using **Fernet encryption**.
- On the **Decrypt Message** page, users can retrieve their encrypted message **if they enter the correct credentials**.

### **Data Visualization**
- Users can generate **plots** based on **selected countries and data types**.
- Available data types include **total cases, deaths, and vaccinated people**.

### **Predictions Page**
- A **machine learning model** predicts **COVID-19 cases** for the next **14 days**.
- Results are displayed in a **table** and **plot**, with an option to **download predictions as a CSV file**.

---

## Setup & Installation

### **Step 1: Generate keys**
Before running the project, generate the required **encryption keys**: ```python generate_key.py```

This script creates a fernet_key.key file. This file contains:
- Django SECRET_KEY (for security)
- Fernet key (for encrypting messages)

I kept them private and I didn't commit them to Git.

### **Step 2: Install dependencies**
Make sure you have Python 3.9+ installed. Then, install all required packages: ```pip install -r requirements.txt```

### **Step 3: Migrations**
Since I ignored migration files in .gitignore, you will need to recreate them. Run:
- ```python manage.py makemigrations```
- ```python manage.py migrate```

### **Step 4: Download the dataset**
The dataset size is quite large so you will need to install it in the root of the project. You can find the dataset here: https://www.kaggle.com/datasets/devinaconley/covid19-owid-data.

### **Step 5: Run the project**
Start the Django development server: ```python manage.py runserver```

---

## Important notes:
- Data was not normalized, and the focus was on the implementation rather than perfect data representation.
- Some plots may not accurately represent COVID-19 trends, as the goal was to test visualization and machine learning tools.
- Translations were written manually, which made adding new languages tedious.

---

## Future improvement:
- Normalize and clean the dataset.
- Improve the accuracy of ML predictions.
- Automate translation generation.
- Enhance data visualization with interactive plots. I attempted to implement interactive plots using Plotly and Dash, but I encountered some issues and decided to move forward without them.