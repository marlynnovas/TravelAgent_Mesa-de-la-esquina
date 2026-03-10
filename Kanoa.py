import flet as ft
import requests

BASE_URL = "https://restcountries.com/v3.1/all?fields=name,capital,region,subregion,population,currencies,languages,flags,timezones"

def get_country_kpi():
    country_name = input("Enter country name: ").strip().lower()
    response = requests.get(BASE_URL)
    countries = response.json()

    #Siempre era un show con lo mismo que daba error porque o se escribia con mayuscula o no. 
    country = next(
        (c for c in countries if country_name in (c.get("name", {}).get("official", "").lower(),
                                                  c.get("name", {}).get("common", "").lower())),
        None
    )