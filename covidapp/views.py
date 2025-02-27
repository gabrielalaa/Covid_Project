from django.shortcuts import render, redirect
from data_analysis import analyze_trends, df_country
from django.utils.translation import gettext as _
from django.utils.translation import activate
from .forms import AccountCreationForm, DecryptMessageForm
from .models import Account
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from django.conf import settings
import os
from sklearn.linear_model import LinearRegression

# Main view for the homepage
def home(request):
    insights = analyze_trends(df_country)
    context = {
        "insights": insights,
        "current_language": request.LANGUAGE_CODE,  # Current language
        "languages": [("en", _("English")), ("ro", _("Romanian"))]  # Available languages
    }
    return render(request, 'covidapp/home.html', context)

# View to switch languages
def switch_language(request, lang_code):
    activate(lang_code)
    return home(request)

#########################################################################################

# View to create an account
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            message = form.cleaned_data['message']

            # Check if username already exists
            if Account.objects.filter(username=username).exists():
                return render(request, 'covidapp/create_account.html', {'form': form, 'error': _('Username already exists!')})

            # Create and save the account
            account = Account(username=username)
            account.set_password(password)
            account.set_message(message)
            account.save()

            return redirect('decrypt_message')  # Redirect to the decryption page
    else:
        form = AccountCreationForm()

    return render(request, 'covidapp/create_account.html', {'form': form})

# View to decrypt a message
def decrypt_message(request):
    if request.method == 'POST':
        form = DecryptMessageForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                account = Account.objects.get(username=username)
                if account.check_password(password):
                    decrypted_message = account.get_message()
                    return render(request, 'covidapp/decrypt_message.html', {'form': form, 'message': decrypted_message})
                else:
                    error = _('Incorrect password!')
            except Account.DoesNotExist:
                error = _('Account not found!')

            return render(request, 'covidapp/decrypt_message.html', {'form': form, 'error': error})
    else:
        form = DecryptMessageForm()

    return render(request, 'covidapp/decrypt_message.html', {'form': form})

#########################################################################################

# Load the dataset
data_path = os.path.join(settings.BASE_DIR, 'owid-covid-data.csv')

# Check if file exists before reading
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = None  # Handle missing data in views

def generate_plots(request):
    plot_path = None
    if request.method == 'POST':
        selected_country = request.POST.get('country')
        selected_data_type = request.POST.get('data_type')

        if not selected_country or not selected_data_type:
            return render(request, 'covidapp/generate_plots.html',
                          {'error': 'Please select a country and data type.', 'countries': df['location'].unique()})

        # Filter data for the selected country
        filtered_data = df[df['location'] == selected_country]
        filtered_data['date'] = pd.to_datetime(filtered_data['date'])  # Ensure 'date' is datetime
        filtered_data = filtered_data[filtered_data['date'] >= '2020-01-01']

        # Plot the selected data
        plt.figure(figsize=(12, 6))
        plt.plot(filtered_data['date'], filtered_data[selected_data_type], label=selected_country)

        plt.title(f"{selected_data_type.capitalize()} for {selected_country}")
        plt.xlabel("Date")
        plt.ylabel(selected_data_type.capitalize())
        plt.legend()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Year-Month format
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Show ticks every 6 months
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot
        plot_path = 'covidapp/single_country_plot.png'
        plot_full_path = os.path.join(settings.STATICFILES_DIRS[0], plot_path)
        plt.savefig(plot_full_path)
        plt.close()

    # Render the page with the plot and countries dropdown
    return render(request, 'covidapp/generate_plots.html',
                  {'plot_path': plot_path, 'countries': df['location'].unique()})

#########################################################################################

# Prediction View
def predictions(request):
    predictions = None
    future_dates = None
    plot_path = None

    if request.method == 'POST':
        country = request.POST.get('country', None)
        if country:
            # Filter data for the selected country
            data = df[df['location'] == country]
            data['date'] = pd.to_datetime(data['date'])
            data['date_ordinal'] = data['date'].map(pd.Timestamp.toordinal)

            if len(data) > 10:
                X = data[['date_ordinal']]
                y = data['total_cases'].fillna(0)

                # train the model
                model = LinearRegression()
                model.fit(X, y)

                # Generate predictions
                future_dates = pd.date_range(start=data['date'].max(), periods=15, freq='D')[1:]
                future_data = pd.DataFrame({'date': future_dates})
                future_data['date_ordinal'] = future_data['date'].map(pd.Timestamp.toordinal)
                future_data['predicted_cases'] = model.predict(future_data[['date_ordinal']])
                predictions = future_data

                # plot the predictions
                plt.figure(figsize=(10, 6))
                plt.plot(data['date'], y, label="Actual Cases")
                plt.plot(future_data['date'], future_data['predicted_cases'], label="Predicted Cases", linestyle="--")
                plt.title(f"COVID-19 Case Predictions for {country}")
                plt.xlabel("Date")
                plt.ylabel("Total Cases")
                plt.legend()
                plt.xticks(rotation=45)
                plt.tight_layout()

                # save the plot
                plot_path = f"covidapp/{country}_predictions.png"
                plot_full_path = os.path.join(settings.STATICFILES_DIRS[0], plot_path)
                plt.savefig(plot_full_path)
                plt.close()

    return render(request, 'covidapp/predictions.html', {
        'predictions': predictions.to_dict('records') if predictions is not None else None,
        'countries': df['location'].unique(),
        'plot_path': plot_path,
    })
