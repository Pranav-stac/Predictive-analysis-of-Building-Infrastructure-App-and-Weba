import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import numpy as np

# Load the dataset
df = pd.read_csv('building_inspection_reports.csv')

# Convert Inspection_Date to datetime
df['Inspection_Date'] = pd.to_datetime(df['Inspection_Date'])

# Feature engineering: Extract year, month, and day from Inspection_Date
df['Year'] = df['Inspection_Date'].dt.year
df['Month'] = df['Inspection_Date'].dt.month
df['Day'] = df['Inspection_Date'].dt.day

# Drop the original Inspection_Date column
df = df.drop(columns=['Inspection_Date'])

# Encode the Building column
df = pd.get_dummies(df, columns=['Building'])

# Define features and target variables
features = df.drop(columns=[
    'Roof_Status', 'Roof_Issue', 'Siding_Status', 'Siding_Issue', 'Windows_Status', 'Windows_Issue',
    'HVAC_Status', 'HVAC_Issue', 'Plumbing_Status', 'Plumbing_Issue', 'Elevators_Status', 'Elevators_Issue',
    'Lighting_Status', 'Lighting_Issue', 'Landscaping_Status', 'Landscaping_Issue', 'Emergency Exits_Status', 'Emergency Exits_Issue'
])
target_columns = [
    'Roof_Status', 'Roof_Issue', 'Siding_Status', 'Siding_Issue', 'Windows_Status', 'Windows_Issue',
    'HVAC_Status', 'HVAC_Issue', 'Plumbing_Status', 'Plumbing_Issue', 'Elevators_Status', 'Elevators_Issue',
    'Lighting_Status', 'Lighting_Issue', 'Landscaping_Status', 'Landscaping_Issue', 'Emergency Exits_Status', 'Emergency Exits_Issue'
]

# Convert target variables to binary (1 if maintenance is required, 0 otherwise)
for col in target_columns:
    df[col] = df[col].apply(lambda x: 1 if x < 3 else 0)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, df[target_columns], test_size=0.2, random_state=42)

# Initialize and train the models for each target variable
models = {}
for target in target_columns:
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train[target])
    models[target] = model

# Function to predict future maintenance requirement
def predict_future_maintenance(building, date):
    date = pd.to_datetime(date)
    year, month, day = date.year, date.month, date.day
    building_encoded = [1 if f'Building_{building}' in col else 0 for col in features.columns if col.startswith('Building_')]
    input_features = [year, month, day] + building_encoded
    
    # Ensure the feature vector has the same length as the training data
    while len(input_features) < len(features.columns):
        input_features.append(0)
    
    predictions = {}
    for target, model in models.items():
        predictions[target] = model.predict([input_features])[0]
    
    return predictions

# Function to find the next maintenance date
def find_next_maintenance_date(building, start_date, end_date):
    current_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    maintenance_dates = []

    while current_date <= end_date:
        predictions = predict_future_maintenance(building, current_date)
        if any(predictions.values()):  # If any maintenance is required
            maintenance_dates.append((current_date, predictions))
        current_date += pd.DateOffset(days=1)

    return maintenance_dates

# Example usage
building = 'Building A'
start_date = '2027-01-01'
end_date = '2027-12-31'
maintenance_dates = find_next_maintenance_date(building, start_date, end_date)

# Print detailed analysis
for date, predictions in maintenance_dates:
    print(f"Predicted Maintenance Requirement for {building} on {date.date()}:")
    for param, value in predictions.items():
        status = "Maintenance Required" if value == 1 else "No Maintenance Required"
        print(f"{param}: {status}")

# Evaluate the models
for target in target_columns:
    y_pred = models[target].predict(X_test)
    print(f"Classification Report for {target}:")
    print(classification_report(y_test[target], y_pred))

# Function to read PDF report
def read_pdf_report(filename):
    doc = fitz.open(filename)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to analyze maintenance report
def analyze_maintenance_report(text):
    lines = text.split('\n')
    maintenance_data = {}
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            maintenance_data[key] = value
    return maintenance_data

# Function to generate analysis report
def generate_analysis_report(maintenance_data, output_filename):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 50, "Maintenance Analysis Report")

    # Add maintenance data to the PDF
    y_position = height - 100
    for key, value in maintenance_data.items():
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, f"{key}: {value}")
        y_position -= 20

    # Save the PDF
    c.save()

# Function to select file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

# Select the PDF file using file picker
selected_file = select_file()
if selected_file:
    # Read and analyze the PDF report
    text = read_pdf_report(selected_file)
    extracted_data = analyze_maintenance_report(text)

    print("Extracted Maintenance Data:")
    for key, value in extracted_data.items():
        print(f"{key}: {value}")

    # Generate analysis report in PDF format
    output_filename = "maintenance_analysis_report.pdf"
    generate_analysis_report(extracted_data, output_filename)
    print(f"Analysis report '{output_filename}' has been created.")
else:
    print("No file selected.")