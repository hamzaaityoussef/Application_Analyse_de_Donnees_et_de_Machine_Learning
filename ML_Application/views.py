from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import *
import pandas as pd
from django.http import JsonResponse
import os
from django.conf import settings
from .forms import FileUploadForm
from .models import Dataset
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import matplotlib.pyplot as plt
import io
import urllib, base64

@login_required(login_url='/login')
def base(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        nom = request.user.last_name if request.user.last_name else "Not provided"
        prenom = request.user.first_name if request.user.first_name else "Not provided"
    else:
        nom = "Guest"
        prenom = "User"

    return render(request, 'base.html', {
        'nom': nom,
        'prenom': prenom,
        'user': request.user,  # Pass the full user object for additional details
    })




# login and logout
def loginpage(request):
    if request.user.is_authenticated:
        
        return redirect('upload')
        

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.password == password:
            
            login(request, user)
            return redirect('upload')    
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe invalide. Veuillez réessayer.')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')

# end login and logout

# home 
def home(request):
    
    print('bnjrjr')
    return render(request, 'home.html')
#end  home 



# upload and delete datasets
@login_required(login_url='/login')
def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']

            # Save the dataset instance
            dataset = Dataset.objects.create(
                name=file.name,
                file=file,
                user=request.user
            )

            # Redirect to refresh the page
            return redirect('upload')

    else:
        form = FileUploadForm()

    # Fetch datasets associated with the logged-in user
    datasets = Dataset.objects.filter(user=request.user)

    return render(request, 'upload.html', {'form': form, 'datasets': datasets})


@login_required
def delete_dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id, user=request.user)

    # Delete the file from storage
    if dataset.file:
        file_path = dataset.file.path
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Delete the database entry
    dataset.delete()

    # Redirect back to the upload page
    return redirect('upload')

#end upload 


# Preprocess 
def Preprocess(request):
    csv_path = r'C:\Users\Asus PC\Downloads\Dataset_lharba.csv'  # Replace with your dataset's path
    df = pd.read_csv(csv_path)
 # Basic Statistics
    row_count = df.shape[0]
    feature_count = df.shape[1]
    missing_values = df.isnull().sum()
    duplicate_rows = df.duplicated().sum()
    data_types = df.dtypes

    # First 5 rows
    head = df.head(10).to_html(classes="table table-light")
   

    return render(request, 'preprocess.html', {
        'head': head,
        'row_count': row_count,
        'feature_count': feature_count,
        'missing_values': missing_values,
        'duplicate_rows': duplicate_rows,
        'data_types': data_types,
        
    })
#end  Preprocess 





# visualisation 
@login_required(login_url='/login')
def visualisation(request):
    # Load your dataset
    csv_path = r'C:\Users\Asus PC\Downloads\Dataset_lharba.csv'  # Replace with your dataset's path
    df = pd.read_csv(csv_path)

    
    categorical_vars = [col for col in df.columns if df[col].nunique() <= 20 and df[col].dtype == 'object']
    continuous_vars = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]

    categorical_sections = {}
    continuous_sections = {}

    # Handle Categorical Sections
    for i, col in enumerate(categorical_vars[:2], start=1):  # Limit to 2 sections
        selected_col = request.GET.get(f'cat_{i}', col)  # Get the specific parameter for each section
        fig, ax = plt.subplots(figsize=(4, 2))
        if i == 1:  # Pie chart for the first categorical variable
            df[selected_col].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
        else:  # Bar chart for the second categorical variable
            df[selected_col].value_counts().plot(kind='bar', ax=ax)

            ax.set_title(f'{selected_col} Distribution')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        categorical_sections[f'cat_{i}'] = {
            'chart_uri': 'data:image/png;base64,' + urllib.parse.quote(base64.b64encode(buf.read())),
            'options': categorical_vars,
            'selected': selected_col,
        }
        buf.close()

    # Handle Continuous Sections
    for i, col in enumerate(continuous_vars[:2], start=1):  # Limit to 2 sections
        selected_col = request.GET.get(f'cont_{i}', col)  # Get the specific parameter for each section
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.scatter(range(len(df[selected_col])), df[selected_col], alpha=0.7, color='blue')
        ax.set_title(f'{selected_col} Scatter Plot')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        continuous_sections[f'cont_{i}'] = {
            'chart_uri': 'data:image/png;base64,' + urllib.parse.quote(base64.b64encode(buf.read())),
            'options': continuous_vars,
            'selected': selected_col,
        }
        buf.close()

    return render(request, 'visualisation.html', {
        'categorical_sections': categorical_sections,
        'continuous_sections': continuous_sections,
    })
    
#end upload 


# modeles 
@login_required(login_url='/login')
def modeles(request):
    
    print('bnjrjr')
    return render(request, 'modeles.html')
#end modeles 


# Predictions 
@login_required(login_url='/login')
def Predictions(request):
    
    print('bnjrjr')
    return render(request, 'Predictions.html')
#end Predictions 


# documentation 
@login_required(login_url='/login')
def documentation(request):
    
    print('bnjrjr')
    return render(request, 'documentation.html')
#end documentation 

# report 
@login_required(login_url='/login')
def report(request):
    
    print('bnjrjr')
    return render(request, 'report.html')
#end report 
