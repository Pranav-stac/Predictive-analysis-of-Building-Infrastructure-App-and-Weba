import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import random  # For generating random months

def generate_maintenance_report_from_pdf(input_pdf_filename):
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
        
        # Identify which repairs are needed
        repairs_needed = [target for target, value in predictions.items() if value == 1]
        
        return predictions, repairs_needed

    # Function to find the next maintenance date
    def find_next_maintenance_date(building, start_date, end_date):
        current_date = pd.to_datetime(start_date) + pd.DateOffset(days=1)  # Start checking from the next day
        end_date = pd.to_datetime(end_date)

        while current_date <= end_date:
            predictions, repairs_needed = predict_future_maintenance(building, current_date)
            if repairs_needed:  # If any maintenance is required
                fine_parameters = [target for target, value in predictions.items() if value == 0]
                return current_date, repairs_needed, fine_parameters
            current_date += pd.DateOffset(days=1)

        return None, [], []

    # Function to generate analysis report
    def generate_analysis_report(building, next_maintenance_date, repairs_needed, fine_parameters, output_filename):
        c = canvas.Canvas(output_filename, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(100, height - 50, f"Maintenance Analysis Report for {building}")

        # Highlighted Maintenance date
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(1, 0, 0)  # Red color for highlighting
        c.drawString(100, height - 80, f"Next Maintenance Date: {next_maintenance_date.date()}")
        c.setFillColorRGB(0, 0, 0)  # Reset to black

        # Draw parameters needing work
        y_position = height - 150
        c.setFont("Helvetica", 12)

        for param in repairs_needed:
            if "Issue" in param:  # Only print parameters related to issues
                c.drawString(90, y_position, f"- {param}")
                y_position -= 20

        c.setFont("Helvetica-Bold", 14)
        c.drawString(400, height - 120, "Parameters in Good Condition:")

        y_position = height - 150
        c.setFont("Helvetica", 12)

        for param in fine_parameters:
            if "Status" in param and param not in repairs_needed:
                c.drawString(390, y_position, f"- {param}")
                y_position -= 20

        c.save()

    # Function to read PDF report
    def read_pdf_report(filename):
        doc = fitz.open(filename)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    # Function to read parameters from PDF, specifically the "Report Date"
    def read_parameters_from_pdf(filename):
        text = read_pdf_report(filename)
        parameters = {}
        lines = text.split('\n')
        for line in lines:
            if ": " in line:
                key, value = line.split(": ", 1)
                parameters[key.strip()] = value.strip()
        return parameters

    parameters = read_parameters_from_pdf(input_pdf_filename)

    # Extract building name and Report Date from the PDF
    building = parameters.get('Building', 'Building A')  # Default to 'Building A' if not found
    
    # Extract Report Date
    report_date_str = parameters.get('Report Date')

    # Convert the extracted Report Date to a valid date
    if report_date_str:
        try:
            start_date = pd.to_datetime(report_date_str)  # Convert the extracted string to a datetime
        except ValueError:
            print(f"Error: The extracted Report Date '{report_date_str}' is not a valid date.")
            start_date = None
    else:
        print("Error: Report Date not found in the PDF report.")
        start_date = None

    # If the Report Date is valid, calculate the end date
    if start_date is not None:
        n = random.randint(1, 11)
        end_date = start_date + pd.DateOffset(years=1, months=n)

        # Generate a new maintenance analysis report based on extracted parameters
        next_maintenance_date, repairs_needed, fine_parameters = find_next_maintenance_date(building, start_date, end_date)

        if next_maintenance_date:
            print(f"Next Maintenance Requirement for {building} on {next_maintenance_date.date()}:")
            print("Parameters Needing Work:")
            for param in repairs_needed:
                print(f"- {param}")

            print("\nParameters in Good Condition:")
            for param in fine_parameters:
                print(f"- {param}")

            output_filename = f"{building}_maintenance_analysis_report.pdf"
            generate_analysis_report(building, next_maintenance_date, repairs_needed, fine_parameters, output_filename)
            print(f"Analysis report '{output_filename}' has been created.")
        else:
            print("No maintenance required within the specified date range.")
    else:
        print("Error: Report Date is missing or invalid. Cannot proceed with maintenance analysis.")

# Initialize Tkinter root (hidden)
root = tk.Tk()
root.withdraw()

# Hard code the path of the input PDF file
input_pdf_filename = r"C:\Users\aniru\Downloads\23_LoremIpsum-main\23_LoremIpsum-main\kavach\media\maintenance_analysis_report.pdf"

# Generate the maintenance report using the hard-coded path
generate_maintenance_report_from_pdf(input_pdf_filename)