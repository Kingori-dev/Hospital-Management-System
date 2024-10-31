from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
import os

# Flask app and SQLite setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
db = SQLAlchemy(app)

# Models for the database
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)

class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    medicine_name = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Doctors Page
@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    if request.method == 'POST':
        name = request.form.get('name')
        specialization = request.form.get('specialization')
        new_doctor = Doctor(name=name, specialization=specialization)
        db.session.add(new_doctor)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('doctors'))
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

# Pharmacy Page
@app.route('/pharmacy', methods=['GET', 'POST'])
def pharmacy():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        new_medicine = Medicine(name=name, quantity=quantity)
        db.session.add(new_medicine)
        db.session.commit()
        flash('Medicine added successfully!', 'success')
        return redirect(url_for('pharmacy'))
    medicines = Medicine.query.all()
    return render_template('pharmacy.html', medicines=medicines)

# Patients Page
@app.route('/patients')
def patients():
    return render_template('patients.html')

# Performance Chart Page
@app.route('/chart')
def chart():
    # For demo, let's create some random data
    data = {'Category': ['Doctors', 'Patients', 'Prescriptions'], 'Count': [len(Doctor.query.all()), 50, 120]}
    fig = px.bar(data, x='Category', y='Count', title='Hospital Performance Metrics')
    chart = fig.to_html(full_html=False)
    return render_template('chart.html', chart=chart)

# Initialize the database
@app.before_request
def create_tables():
    if not hasattr(app, 'has_run'):
        db.create_all()
        app.has_run = True


if __name__ == '__main__':
    app.run(debug=True)
