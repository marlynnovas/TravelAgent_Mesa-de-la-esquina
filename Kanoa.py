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

    if not country:
        print("Country not found.")
        return

    name = country["name"]["official"]
    capital = country.get("capital", ["N/A"])[0]
    region = country.get("region", "N/A")
    subregion = country.get("subregion", "N/A")
    population = country.get("population", 0)
    timezones = ", ".join(country.get("timezones", []))
    flag = country.get("flags", {}).get("png", "N/A")

    currencies = country.get("currencies", {})
    if currencies:
        first_currency = list(currencies.values())[0].get("name", "N/A")
    else:
        first_currency = "N/A"
        print("\n===== COUNTRY Information =====")
        print("\n===== COUNTRY Information =====")
    print(f"Name: {name}")
    print(f"Capital: {capital}")
    print(f"Region / Subregion: {region} / {subregion}")
    print(f"Population: {population:,}")
    print(f"Currency: {first_currency}")
    print(f"Languages: {languages_str}")
    print(f"Time Zones: {timezones}")
    print(f"Flag: {flag}")
    print("=======================\n")

