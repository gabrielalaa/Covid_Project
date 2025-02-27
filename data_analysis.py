import os
import django
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from django.utils.translation import gettext as _

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Covid_Project.settings")
django.setup()

# Load data
data_path = "owid-covid-data.csv"
df = pd.read_csv(data_path)

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Filter data for Romania
df_country = df[df["location"] == "Romania"]

# Drop rows with missing values in important columns
df_country = df_country.dropna(subset=["total_deaths", "total_cases", "date"])

# Add mortality_rate column
df_country["mortality_rate"] = df_country["total_deaths"] / df_country["total_cases"]

# Function to generate the COVID-19 evolution plot
def generate_covid_plot(data):
    plt.figure(figsize=(10, 5))
    plt.plot(data["date"], data["total_cases"], label=_("Total Cases"))
    plt.plot(data["date"], data["total_deaths"], label=_("Total Deaths"))
    plt.title(_("COVID-19 Evolution in Romania"))
    plt.xlabel(_("Date"))
    plt.ylabel(_("Number of cases"))
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("covidapp/static/covidapp/covid_plot.png")
    print(_("COVID-19 evolution plot saved!"))

# Function to generate the vaccination progress plot
def generate_vaccination_plot(data):
    plt.figure(figsize=(10, 5))
    plt.plot(data["date"], data["people_vaccinated"], label=_("People Vaccinated"))
    plt.plot(data["date"], data["people_fully_vaccinated"], label=_("Fully Vaccinated"))
    plt.title(_("Vaccination Progress in Romania"))
    plt.xlabel(_("Date"))
    plt.ylabel(_("Number of Vaccinations"))
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("covidapp/static/covidapp/vaccination_plot.png")
    print(_("Vaccination plot saved!"))

# Analyze trends and generate insights
def analyze_trends(data):
    avg_mortality = data["mortality_rate"].mean()
    recent_cases = data["total_cases"].iloc[-1]
    recent_deaths = data["total_deaths"].iloc[-1]

    insights = _(
        "Average mortality rate is {avg_mortality:.2%}. Total cases are {recent_cases:,}, with {recent_deaths:,} deaths."
    ).format(avg_mortality=avg_mortality, recent_cases=recent_cases, recent_deaths=recent_deaths)

    if recent_deaths / recent_cases < 0.01:
        insights += " " + _("It seems the number of deaths is relatively low compared to cases.")
    else:
        insights += " " + _("The mortality rate is concerning.")

    return insights

# Generate plots
generate_covid_plot(df_country)
generate_vaccination_plot(df_country)
