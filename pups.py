import flet as ft
import requests

# URL de búsqueda por nombre
SEARCH_URL = "https://restcountries.com/v3.1/name/"

def main(page: ft.Page):
    page.title = "CARICOM Travel Agency"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 1200
    page.window_height = 900
    page.scroll = "auto"

    # Referencias
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
        # 1. Obtener el valor usando .current
        country_name = country_input.current.value.strip()

        if not country_name:
            error_box.current.content = ft.Text("Please enter a country name.", color=ft.Colors.RED)
            error_box.current.visible = True
            page.update()
            return

        error_box.current.visible = False
        page.update()

        try:
            # Petición a la API
            response = requests.get(f"{SEARCH_URL}{country_name}")
            if response.status_code != 200:
                raise Exception("Country not found.")
            
            country = response.json()[0]

            # Datos Básicos
            name = country["name"]["official"]
            capital = country.get("capital", ["N/A"])[0]
            region = country.get("region", "N/A")
            pop = country.get("population", 0)
            
            # Clima (Open-Meteo)
            latlng = country.get("latlng", [0, 0])
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latlng[0]}&longitude={latlng[1]}&current_weather=true"
            weather_res = requests.get(weather_url).json()
            temp = weather_res.get("current_weather", {}).get("temperature", "N/A")
            wind = weather_res.get("current_weather", {}).get("windspeed", "N/A")

            # Moneda
            currencies = country.get("currencies", {})
            first_curr = list(currencies.values())[0].get("name", "N/A") if currencies else "N/A"

            # --- CORRECCIÓN AQUÍ: Usar .current.content ---
            info_section.current.content = ft.Column([
                ft.Text(f"Country: {name}", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Divider(),
                ft.Row([
                    ft.Container(content=ft.Column([ft.Text("Capital"), ft.Text(capital, weight="bold")]), 
                                 padding=15, bgcolor=ft.Colors.BLUE_50, border_radius=10, expand=True),
                    ft.Container(content=ft.Column([ft.Text("Region"), ft.Text(region, weight="bold")]), 
                                 padding=15, bgcolor=ft.Colors.GREEN_50, border_radius=10, expand=True),
                    ft.Container(content=ft.Column([ft.Text("Population"), ft.Text(f"{pop:,}", weight="bold")]), 
                                 padding=15, bgcolor=ft.Colors.RED_50, border_radius=10, expand=True),
                ]),
                ft.Row([
                    ft.Container(content=ft.Column([ft.Text("Currency"), ft.Text(first_curr, weight="bold")]), 
                                 padding=15, bgcolor=ft.Colors.PURPLE_50, border_radius=10, expand=True),
                    ft.Container(content=ft.Column([ft.Text("Weather"), ft.Text(f"{temp}°C | Wind {wind}km/h", weight="bold")]), 
                                 padding=15, bgcolor=ft.Colors.AMBER_50, border_radius=10, expand=True),
                ])
            ], spacing=15)
            
            # --- CORRECCIÓN AQUÍ: Usar .current.visible ---
            info_section.current.visible = True
            
        except Exception as ex:
            error_box.current.content = ft.Text(f"Error: {str(ex)}", color=ft.Colors.RED)
            error_box.current.visible = True
            info_section.current.visible = False
        
        page.update()

    def add_plan(e):
        try:
            days = int(duration_input.current.value)
            cost = (days * 100) + 350
            
            plans_table.current.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(client_name.current.value)),
                    ft.DataCell(ft.Text(country_input.current.value)),
                    ft.DataCell(ft.Text(str(days))),
                    ft.DataCell(ft.Text(notes_input.current.value)),
                    ft.DataCell(ft.Text(f"${cost}")),
                ])
            )
            client_name.current.value = ""
            duration_input.current.value = ""
            notes_input.current.value = ""
            page.update()
        except:
            pass

    # Layout Principal
    page.add(
        ft.Column([
            ft.Text("CARICOM Travel Agency", size=40, weight="bold", color="blue700"),
            ft.Text("Explore destinations and insights", size=16, color="grey600"),
            
            ft.Row([
                ft.TextField(ref=country_input, label="Country Name", width=300, on_submit=search_country),
                ft.Dropdown(ref=time_range_dropdown, label="Time", width=150, value="30 days",
                            options=[ft.dropdown.Option("1 week"), ft.dropdown.Option("30 days")]),
                ft.ElevatedButton("Search", icon=ft.Icons.SEARCH, on_click=search_country),
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Container(ref=error_box, visible=False),
            # El contenedor que empieza invisible
            ft.Container(ref=info_section, visible=False, padding=20, border=ft.border.all(1, "grey300"), border_radius=15),
            
            ft.Divider(height=50),
            
            ft.Text("Trip Planning", size=28, weight="bold", color="blue700"),
            ft.Row([
                ft.TextField(ref=client_name, label="Client Name", expand=True),
                ft.TextField(ref=duration_input, label="Days", width=100),
            ]),
            ft.TextField(ref=notes_input, label="Notes / Requirements", multiline=True),
            ft.ElevatedButton("Add to Plan", icon=ft.Icons.ADD, on_click=add_plan),
            
            ft.DataTable(
                ref=plans_table,
                columns=[
                    ft.DataColumn(ft.Text("Client")),
                    ft.DataColumn(ft.Text("Country")),
                    ft.DataColumn(ft.Text("Days")),
                    ft.DataColumn(ft.Text("Notes")),
                    ft.DataColumn(ft.Text("Cost")),
                ]
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)