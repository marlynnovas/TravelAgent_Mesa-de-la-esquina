import flet as ft
import requests

BASE_URL = "https://restcountries.com/v3.1/all?fields=name,capital,region,subregion,population,currencies,languages,flags,timezones,latlng"

# Lista en memoria para guardar planes de viaje
travel_plans = []

def get_country_kpi():
    country_name = input("Enter country name: ").strip().lower()
    response = requests.get(BASE_URL)
    countries = response.json()

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

    languages = country.get("languages", {})
    if languages:
        lang_list = [v if isinstance(v, str) else v.get("name","N/A") for v in languages.values()]
        languages_str = ", ".join(lang_list)
    else:
        languages_str = "N/A"

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

def main(page: ft.Page):

    page.title = "CARICOM Travel Agency"
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

    # Referencias para planificación
    client_name = ft.Ref[ft.TextField]()
    duration_input = ft.Ref[ft.TextField]()
    notes_input = ft.Ref[ft.TextField]()
    plans_table = ft.Ref[ft.DataTable]()

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

        latlng = country.get("latlng", [0, 0])
        lat = latlng[0]
        lon = latlng[1]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_data = requests.get(weather_url).json()

        temperature = weather_data.get("current_weather", {}).get("temperature", "N/A")
        windspeed = weather_data.get("current_weather", {}).get("windspeed", "N/A")

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
            ft.Text(f"Country: {name}", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Text(f"Date Range Selected: {selected_range}", size=14, color=ft.Colors.GREY_700),
            ft.Divider(),
            ft.Row([
                ft.Container(content=ft.Column([
                    ft.Text("Capital", size=12, color=ft.Colors.GREY_600),
                    ft.Text(capital, size=18, weight=ft.FontWeight.BOLD)
                ]), padding=20, bgcolor=ft.Colors.BLUE_50, border_radius=12, expand=True),
                ft.Container(content=ft.Column([
                    ft.Text("Region / Subregion", size=12, color=ft.Colors.GREY_600),
                    ft.Text(f"{region} / {subregion}", size=18, weight=ft.FontWeight.BOLD)
                ]), padding=20, bgcolor=ft.Colors.GREEN_50, border_radius=12, expand=True),
                ft.Container(content=ft.Column([
                    ft.Text("Population", size=12, color=ft.Colors.GREY_600),
                    ft.Text(f"{population:,}", size=18, weight=ft.FontWeight.BOLD)
                ]), padding=20, bgcolor=ft.Colors.RED_50, border_radius=12, expand=True),
                ft.Container(content=ft.Column([
                    ft.Text("Currency", size=12, color=ft.Colors.GREY_600),
                    ft.Text(first_currency, size=18, weight=ft.FontWeight.BOLD)
                ]), padding=20, bgcolor=ft.Colors.PURPLE_50, border_radius=12, expand=True),
            ], spacing=15),
            ft.Container(height=15),

            ft.Row([
                ft.Container(content=ft.Column([
                    ft.Text("Languages", size=12, color=ft.Colors.GREY_600),
                    ft.Text(languages_str, size=16, weight=ft.FontWeight.BOLD)
                ]), padding=20, bgcolor=ft.Colors.ORANGE_50, border_radius=12, expand=True),

                ft.Container(content=ft.Column([
                    ft.Text("Time Zones", size=12, color=ft.Colors.GREY_600),
                    ft.Text(timezones, size=16, weight=ft.FontWeight.BOLD)
                ]), padding=20, bgcolor=ft.Colors.TEAL_50, border_radius=12, expand=True),

                ft.Container(content=ft.Column([
                    ft.Text("Weather", size=12, color=ft.Colors.GREY_600),
                    ft.Text(f"{temperature}°C | Wind {windspeed} km/h", size=16, weight=ft.FontWeight.BOLD)
                ]), padding=20, bgcolor=ft.Colors.AMBER_50, border_radius=12, expand=True),
            ], spacing=15),

            ], spacing=15)

        info_section.current.visible = True
        page.update()

    # --- Función agregar plan ---
    def add_plan(e):
        client = client_name.current.value
        country = country_input.current.value
        try:
            days = int(duration_input.current.value)
        except:
            days = 0
        notes = notes_input.current.value

        cost = days * 100 + 200 + 150

        travel_plans.append({
            "client": client,
            "country": country,
            "days": days,
            "notes": notes,
            "cost": cost
        })

        plans_table.current.rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(client)),
                ft.DataCell(ft.Text(country)),
                ft.DataCell(ft.Text(str(days))),
                ft.DataCell(ft.Text(notes)),
                ft.DataCell(ft.Text(f"${cost}"))
            ])
        )
        page.update()

    # ===== UI DESIGN ===== 
    page.add(

        ft.Column([

            ft.Text("CARICOM Travel Agency",
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                    text_align=ft.TextAlign.CENTER),

            ft.Text("Explore Caribbean destinations and discover detailed country insights",
                    size=16,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER),

            ft.Container(height=20),

            ft.Row([
                ft.TextField(ref=country_input, label="Country Name", width=300, on_submit=search_country),
                ft.Dropdown(ref=time_range_dropdown, label="Time Range", width=180, value="30 days",
                            options=[ft.dropdown.Option("1 week"), ft.dropdown.Option("30 days"),
                                     ft.dropdown.Option("90 days"), ft.dropdown.Option("1 year")]),
                ft.ElevatedButton("Look for Country", icon=ft.Icons.SEARCH, on_click=search_country),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),

            ft.Container(height=30),
            ft.Container(ref=error_box, visible=False),
            ft.Container(ref=info_section, visible=False),

            # --- BLOQUE EXTRA: Trip Planning ---
            ft.Divider(),
            ft.Text("Trip Planning", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.TextField(ref=client_name, label="Client Name", width=300),
            ft.TextField(ref=duration_input, label="Duration (days)", width=200),
            ft.TextField(ref=notes_input, label="Notes / Requirements", width=400),
            ft.ElevatedButton("Add to Plan", icon=ft.Icons.ADD, on_click=add_plan),
            ft.Container(height=20),
            ft.DataTable(
                ref=plans_table,
                columns=[
                    ft.DataColumn(ft.Text("Client")),
                    ft.DataColumn(ft.Text("Country")),
                    ft.DataColumn(ft.Text("Days")),
                    ft.DataColumn(ft.Text("Notes")),
                    ft.DataColumn(ft.Text("Estimated Cost")),
                ],
                rows=[]
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10)   # <-- cierre del Column

    )   # <-- cierre del page.add

if __name__ == "__main__":
    ft.app(target=main)
