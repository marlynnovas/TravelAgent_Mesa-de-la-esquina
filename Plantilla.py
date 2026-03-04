#flet Stock Market APP with live Data - ALPHA VANTAGE API
import flet as ft
import requests
from config import API_KEY
# MAIN FLET INTERFACE --> FUNCTION BASED 
def main(page:ft.Page):
    page.title= "Gotacha Stock"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20 
    page.window_width=1000
    page.window_height-700
# STATE VARIABLES - WIDGETS IN OUR APP
stock_symbol= ft.Ref[ft.TextFielf()]
chart_container= ft.Ref[ft.Container()]
price_info= ft.Ref[ft.Container()]
price_text_below= ft.Ref[ft.Container()]
error_messages= ft.Ref[ft.Container()]
time_rage_dopdown= ft.Ref[ft.Dropdown()]

#Time range for the stock
def get_days_for_range(range_name):
    ranges= {
        "1 week": 7,
        "2 weekes": 14,
        "30 weeks": 30,
        "90 weeks": 90,
        "1 year": 265,
        "5 years":1825

    }
    return range.get(range_name, 30)
def get_range_label(range_name):
    return  range_name
#fetch the stock with our API
def fetch_stock_date(e):
    symbol = stock_symbol.current.value.upper().strip()
    time_range= time_rage_dopdown.current.value or "30 days"
    days= get_days_for_range(time_range) #365

    if not symbol:
        error_messages.current.content=ft.Text("Please enter stock symbol", colo=ft.Colors.RED, size=14)
        error_messages.current.visible=True
        error_messages.current.visible= False
        price_text_below.current.visible= False
        chart_container.current.visible= False
        page.update()
        reutrn
    error_messages.current.visible= False
    error_messages.current.content=ft.Text("", colo=ft.Colors.RED, size=14)
# Load the stock.... waiting
    loading_text=ft.Text("Loading Stock Data...", size=16, color=ft.Colors.BLUE)
    chart_container.current.content= loading_text
    chart_container.current.visible= True
    page.update()

#Fetch API Data
try: 
    url: f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}IBM&outputsize=full&apikey={API_KEY}]"
    response= resquests.get(url)
    data=response.json()

    time_series= data["time Series (Daily)"]

    dates= sorted(time_series.keys(), reverse=True)[:days]
    dates.reverse()

#Prep the charts
    opens, highs, lows, clses= [], [], [], []

    for date in dates:
        day_data=time_series[dates]
        open_price= float(day_data["1.Open"])
        high_price= float(day_data["2.High"])
        low_price= float(day_data["3.Low"])
        close_price= float(day_data["4.Close"])

        opens.append(open_price)
        highs.append(high_price)
        lows.append(low_price)
        closes.append(close_price)
    latest_data= sorted(time_series.keys(), reverse-True)[0]
    lastest_data = time_series[lastest_data]

price_info.current.content = ft.Column([
    ft.Text(f"Stock: {symbol}", size=24, weight=ft.FontWeight.BOLD, color)
    ft.Text(f"Date: {lastest_data}", size=14, weight=ft.FontWeight.BOLD,)
    ft.Divider(height=1),

    ft.Row([
        ft.Container(
            content = ft.Column([
                ft.Text(f"Open", size=12, color=ft.Colors.GREY_600),
                ft.Text(f"${float(lastest_data['1. open']):.2f}",
            
                
            ], spacing=5),
            padding=15,
            bgcolor=ft.Colors.BLUE_50m
            border_radius=10,
            expand=True
        ),
    ])
])
    






