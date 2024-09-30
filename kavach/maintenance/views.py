import os
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import random  # For generating random months
import google.generativeai as genai
import matplotlib.pyplot as plt
import io
import base64

# Configure Gemini API
genai.configure(api_key="AIzaSyCYYf5ZufzvO1tofhFJDSl_yc_FocCHJCA")

# Existing index function
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def real_time_monitoring(request):
    return render(request, 'real_time_monitoring.html')

def automated_alerts(request):
    return render(request, 'automated_alerts.html')

def report_page(request):
    return render(request, 'report_detail.html')

def data_analytics(request):
    return render(request, 'data_analytics.html')

def safety_assurance(request):
    return render(request, 'safety_assurance.html')

# Function to generate the maintenance report and store the information
def generate_maintenance_report_from_pdf(input_pdf_filename):
    df = pd.read_csv(r'E:\Pranav\Hackathons\23_LoremIpsum\building_inspection_reports.csv')
    df['Inspection_Date'] = pd.to_datetime(df['Inspection_Date'])

    # Feature engineering
    df['Year'] = df['Inspection_Date'].dt.year
    df['Month'] = df['Inspection_Date'].dt.month
    df['Day'] = df['Inspection_Date'].dt.day
    df = df.drop(columns=['Inspection_Date'])

    # One-hot encode the Building column
    df = pd.get_dummies(df, columns=['Building'])

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

    # Binary encode
    for col in target_columns:
        df[col] = df[col].apply(lambda x: 1 if x < 3 else 0)

    X_train, X_test, y_train, y_test = train_test_split(features, df[target_columns], test_size=0.2, random_state=42)

    models = {}
    for target in target_columns:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train[target])
        models[target] = model

    def predict_future_maintenance(building, date):
        date = pd.to_datetime(date)
        year, month, day = date.year, date.month, date.day
        building_encoded = [1 if f'Building_{building}' in col else 0 for col in features.columns if col.startswith('Building_')]
        input_features = [year, month, day] + building_encoded

        while len(input_features) < len(features.columns):
            input_features.append(0)

        predictions = {}
        for target, model in models.items():
            predictions[target] = model.predict([input_features])[0]

        repairs_needed = [target for target, value in predictions.items() if value == 1]
        return predictions, repairs_needed

    def find_next_maintenance_date(building, start_date, end_date):
        current_date = pd.to_datetime(start_date) + pd.DateOffset(days=1)
        end_date = pd.to_datetime(end_date)

        while current_date <= end_date:
            predictions, repairs_needed = predict_future_maintenance(building, current_date)
            if repairs_needed:
                fine_parameters = [target for target, value in predictions.items() if value == 0]
                return current_date, repairs_needed, fine_parameters
            current_date += pd.DateOffset(days=1)

        return None, [], []

    def generate_bar_and_pie_chart(repairs_needed, fine_parameters):
        # Bar chart for repairs needed
        issues = [param.split('_')[0] for param in repairs_needed]
        counts = {issue: issues.count(issue) for issue in set(issues)}

        plt.figure(figsize=(5, 3))
        plt.bar(counts.keys(), counts.values())
        plt.title('Issues Needing Attention')
        plt.ylabel('Count')

        bar_io = io.BytesIO()
        plt.savefig(bar_io, format='png')
        bar_io.seek(0)
        bar_chart_base64 = base64.b64encode(bar_io.getvalue()).decode('utf8')
        plt.close()  # Close the figure to avoid overlap with the next plot

        # Pie chart for fine parameters
        total_params = len(repairs_needed) + len(fine_parameters)
        fine_percentage = len(fine_parameters) / total_params * 100 if total_params > 0 else 0

        plt.figure(figsize=(4, 4))
        plt.pie([100 - fine_percentage, fine_percentage], labels=['Needs Fixing', 'Fine'], autopct='%1.1f%%')
        plt.title('Condition of Parameters')

        pie_io = io.BytesIO()
        plt.savefig(pie_io, format='png')
        pie_io.seek(0)
        pie_chart_base64 = base64.b64encode(pie_io.getvalue()).decode('utf8')
        plt.close()  # Close the figure to avoid overlap with the next plot

        # Line graph for trends over time (dummy data example)
        months = list(range(1, 13))  # Month numbers
        values = [random.randint(1, 10) for _ in months]  # Example data for each month

        plt.figure(figsize=(8, 4))
        plt.plot(months, values, marker='o')
        plt.title('Monthly Repairs Needed')
        plt.xlabel('Months')
        plt.ylabel('Number of Repairs Needed')
        plt.xticks(months)
        plt.grid()

        line_io = io.BytesIO()
        plt.savefig(line_io, format='png')
        line_io.seek(0)
        line_chart_base64 = base64.b64encode(line_io.getvalue()).decode('utf8')
        plt.close()  # Close the figure

        return bar_chart_base64, pie_chart_base64, line_chart_base64

    def read_pdf_report(filename):
        doc = fitz.open(filename)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    

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
    building = parameters.get('Building', 'Building A')

    report_date_str = parameters.get('Report Date')
    if report_date_str:
        start_date = pd.to_datetime(report_date_str)
    else:
        start_date = None

    if start_date is not None:
        n = random.randint(1, 11)
        end_date = start_date + pd.DateOffset(years=1, months=n)
        next_maintenance_date, repairs_needed, fine_parameters = find_next_maintenance_date(building, start_date, end_date)

        if next_maintenance_date:
            bar_chart_base64, pie_chart_base64, line_chart_base64 = generate_bar_and_pie_chart(repairs_needed, fine_parameters)

            return {
                'next_maintenance_date': next_maintenance_date,
                'repairs_needed': repairs_needed,
                'fine_parameters': fine_parameters,
                'bar_chart_base64': bar_chart_base64,
                'pie_chart_base64': pie_chart_base64,
                'line_chart_base64': line_chart_base64,  # Include line graph
            }
        else:
            return None
    else:
        return None

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf_file = request.FILES['pdf']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        absolute_file_path = os.path.join(settings.MEDIA_ROOT, filename)

        report_data = generate_maintenance_report_from_pdf(absolute_file_path)
        if report_data:
            return render(request, 'report_detail.html', report_data)
        else:
            return render(request, 'report_detail.html', {'error': 'No maintenance data found.'})
    return render(request, 'upload.html')




from rest_framework import viewsets
from .models import Complaint
from .serializers import ComplaintSerializer

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

from django.shortcuts import render, get_object_or_404
from .models import Complaint



def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    # Configure Gemini LLM
    genai.configure(api_key="AIzaSyCYYf5ZufzvO1tofhFJDSl_yc_FocCHJCA")
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Prepare the content to be analyzed
    complaint_info = f"Complaint ID: {complaint.id}\nDescription: {complaint.description}"
    if complaint.image:
        complaint_info += f"\nImage URL: {request.build_absolute_uri(complaint.image.url)}"
    
    # Analyze the complaint using Gemini
    analysis_response = model.generate_content(f"Analyze the following complaint details:\n{complaint_info}")
    
    # Pass the analysis result to the template
    return render(request, 'complaint_detail.html', {
        'complaint': complaint,
        'analysis_result': analysis_response.text  # Pass the analysis result
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from plyer import notification

@api_view(['POST'])
def upload_complaint(request):
    if request.method == 'POST':
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Show notification
            notification.notify(
                title='New Complaint Added',
                message='A new complaint has been successfully added.',
                app_name='Complaint Management System',
                timeout=10  # Notification will disappear after 10 seconds
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)