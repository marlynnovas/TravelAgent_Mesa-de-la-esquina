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

#def main():
#     while True:
#         choice = input("1. Country search & Information \n2. Trip Planning and  Costo estimations \nChoose: ").strip()
#         if choice == "1":
#             get_country_kpi()
#         elif choice == "2":
#             break
#         else:
#             print("Invalid option.")

def main(page: ft.Page):
    page.title = "CANOA Travel Agency"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 1200
    page.window_height = 800
    page.scroll = "auto"

        # References
    country_input = ft.Ref[ft.TextField]()
    time_range_dropdown = ft.Ref[ft.Dropdown]()
    info_section = ft.Ref[ft.Container]()
    error_box = ft.Ref[ft.Container]()

    def search_country(e):

        country_name = country_input.current.value.strip().lower()
        selected_range = time_range_dropdown.current.value

        if not country_name:
            error_box.current.content = ft.Text(
                "Please enter a country name.",
                color=ft.Colors.RED
            )
            error_box.current.visible = True
            page.update()
            return

        response = requests.get(BASE_URL)
        countries = response.json()
        
        # YOUR EXACT MATCHING LOGIC
        country = next(
            (c for c in countries if country_name in (
                c.get("name", {}).get("official", "").lower(),
                c.get("name", {}).get("common", "").lower()
            )),
            None
        )

        if not country:
            error_box.current.content = ft.Text(
                "Country not found.",
                color=ft.Colors.RED
            )
            error_box.current.visible = True
            info_section.current.visible = False
            page.update()
            return

        error_box.current.visible = False

        name = country["name"]["official"]
        capital = country.get("capital", ["N/A"])[0]
        region = country.get("region", "N/A")
        subregion = country.get("subregion", "N/A")
        population = country.get("population", 0)
        timezones = ", ".join(country.get("timezones", []))

        currencies = country.get("currencies", {})
        if currencies:
            first_currency = list(currencies.values())[0].get("name", "N/A")
        else:
            first_currency = "N/A"

        languages = country.get("languages", {})
        if languages:
            lang_list = [v if isinstance(v, str) else v.get("name","N/A") for v in languages.values()]
            languages_str = ", ".join(lang_list)
        else:
            languages_str = "N/A"

        info_section.current.content = ft.Column([

            ft.Text(f"Country: {name}",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700),

            ft.Text(f"Date Range Selected: {selected_range}",
                    size=14,
                    color=ft.Colors.GREY_700),

            ft.Divider(),

            ft.Row([

                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Capital", size=12, color=ft.Colors.GREY_600),
                        ft.Text(capital, size=18, weight=ft.FontWeight.BOLD)
                    ], spacing=5),
                    padding=20,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=12,
                    expand=True
                ),

                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Region / Subregion", size=12, color=ft.Colors.GREY_600),
                        ft.Text(f"{region} / {subregion}", size=18, weight=ft.FontWeight.BOLD)
                    ], spacing=5),
                    padding=20,
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=12,
                    expand=True
                ),

                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Population", size=12, color=ft.Colors.GREY_600),
                        ft.Text(f"{population:,}", size=18, weight=ft.FontWeight.BOLD)
                    ], spacing=5),
                    padding=20,
                    bgcolor=ft.Colors.RED_50,
                    border_radius=12,
                    expand=True
                ),

                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Currency", size=12, color=ft.Colors.GREY_600),
                        ft.Text(first_currency, size=18, weight=ft.FontWeight.BOLD)
                    ], spacing=5),
                    padding=20,
                    bgcolor=ft.Colors.PURPLE_50,
                    border_radius=12,
                    expand=True
                ),

                

            ], spacing=15),

            ft.Container(height=15),

            ft.Text(f"Languages: {languages_str}", size=14),
            ft.Text(f"Time Zones: {timezones}", size=14),

        ], spacing=15)

        info_section.current.visible = True
        page.update()