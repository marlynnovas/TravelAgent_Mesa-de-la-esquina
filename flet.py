import flet as ft
import requests
import datetime
from Travelagent import *

def main(page: ft.Page):
    page.title= "CARICOM Travel Agency"
    page.theme_mode= ft.ThemeMode.LIGHT
    page.padding= 20
    page.window_width= 1000
    page.window_height= 700

    country_Search= ft.Ref[ft.TextField()]
    Arrival_date= ft.Ref[ft.Dropdown()]
    Departure_date=ft.Ref[ft.Dropdown()]
    country_Name=ft.Ref[ft.Container()]
    capital_City=ft.Ref[ft.Container()]
    region_sub=ft.Ref[ft.Container()]
    Population=ft.Ref[ft.Container()]
    Currency=ft.Ref[ft.Container()]
    Languages=ft.Ref[ft.Container()]
    Flag=ft.Ref[ft.Container()]
    Timezone=ft.Ref[ft.Container()]

    def get_days_for_travel():
        today = datetime.datetime.now()

        def handle_change(e: ft.Event[ft.DatePicker]):
            page.add(ft.Text(f"Date changed: {e.control.value.strftime('%m/%d/%Y')}"))

        def handle_dismissal(e: ft.Event[ft.DialogControl]):
            page.add(ft.Text("DatePicker dismissed"))

        d = ft.DatePicker(
            first_date=datetime.datetime(year=today.year - 1, month=1, day=1),
            last_date=datetime.datetime(year=today.year + 1, month=today.month, day=20),
            on_change=handle_change,
            on_dismiss=handle_dismissal,
        )
        return d

    def display_country_data(countries):
        name = country_Name.current.value.strip().upper() if country_Name.current.value else None

        if not name:
            error_messages.current.content = ft.Text(
                "Please enter the country name",
                color=ft.Colors.RED,
                size=14
            )
            error_messages.current.visible = True
            chart_container.current.visible = False
            page.update()
            return

        # Try to find the country
        country = find_country(countries, name)
        if not country:
            page.add(ft.Text("Country not found.", color=ft.Colors.RED))
            return

        # Placeholder for traveling time
        traveling_time = Arrival_date.current.value or "15 days"

        # Loading message
        loading_info = ft.Text("Loading Country information...", size=16, color=ft.Colors.BLUE)
        page.add(loading_info)

        # Add DatePicker button
        d = get_days_for_travel()
        page.add(
            ft.Button(
                content="Pick date",
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: page.show_dialog(d),
            )
        )

    price_info.current.content = ft.Column(
        controls=[

            # Title
            ft.Text(
                f"Official Country Name: {country_name}",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),

            ft.Text(
                f"Capital City: {capital}",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),

            # Info Cards Row
            ft.Row(
                controls=[

                    # Region
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Region", size=12, color=ft.Colors.GREY_600),
                            ft.Text(region, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ], spacing=5),
                        padding=15,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        expand=True,
                    ),

                    # Subregion
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Subregion", size=12, color=ft.Colors.GREY_600),
                            ft.Text(subregion, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ], spacing=5),
                        padding=15,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        expand=True,
                    ),

                    # Population
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Population", size=12, color=ft.Colors.GREY_600),
                            ft.Text(f"{population:,}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ], spacing=5),
                        padding=15,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        expand=True,
                    ),

                    # Currency
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Currency", size=12, color=ft.Colors.GREY_600),
                            ft.Text(
                                ", ".join([v.get("name","N/A") for v in currencies.values()]),
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900,
                            ),
                        ], spacing=5),
                        padding=15,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        expand=True,
                    ),

                    # Languages
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Languages", size=12, color=ft.Colors.GREY_600),
                            ft.Text(
                                ", ".join(languages.values()),
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900,
                            ),
                        ], spacing=5),
                        padding=15,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        expand=True,
                    ),

                    # Time Zones
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Time Zones", size=12, color=ft.Colors.GREY_600),
                            ft.Text(
                                ", ".join(timezones),
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900,
                            ),
                        ], spacing=5),
                        padding=15,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                        expand=True,
                    ),

                ],
                spacing=10,
            ),

            # Flag below
            ft.Image(
                src=flag_url,
                width=200,
                height=120,
                fit=ft.ImageFit.CONTAIN,
            ),
        ],
        spacing=20,
    )  
    # "zone(s) {symbol}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)
    # Load the information . . waiting 
    loadint_info= ft.Text ("Loading Country information", sixe= 16, color=ft.Colors.BLUE)


    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_change(e: ft.Event[ft.DatePicker]):
        page.add(ft.Text(f"Date changed: {e.control.value.strftime('%m/%d/%Y')}"))

    def handle_dismissal(e: ft.Event[ft.DialogControl]):
        page.add(ft.Text("DatePicker dismissed"))

    today = datetime.datetime.now()

    d = ft.DatePicker(
        first_date=datetime.datetime(year=today.year - 1, month=1, day=1),
        last_date=datetime.datetime(year=today.year + 1, month=today.month, day=20),
        on_change=handle_change,
        on_dismiss=handle_dismissal,
    )

    page.add(
        ft.Button(
            content="Pick date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.show_dialog(d),
        )
    )
