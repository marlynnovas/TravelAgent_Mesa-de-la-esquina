import notofficialll as ft 
import requests 

from config import API_KEY 

#main flet

def main(page: ft.Page): 
page.title = "Kayak"
page.theme_mode = ft.ThemeMode.LIGHT 
page.padding = 20 
page.window_width = 2000
page.window_height = 700

stock_symbol = ft.Ref[ft.TextField ()]
chart_container = ft.Ref[ft.Container()]
price_info = ft.Ref[ft.Container()]
price_text_below = ft.Ref [ft.Container()]
error_massages = ft.Ref [ft.Container()]
time_range_dropdown = ft.Ref[ft.Dropdown()]
        
def get_days_for_range(range_name):
    ranges = {
        "1 week": 7, 
        "2 weeks": 14,
        "30 days": 30,
        "90 days": 90,
        "1 year": 365,
        "5 years": 1825,
    }
    return ranges.get(range_name, 30)

def get_range_label(range_name):
        return range_name 
        
def fetch_stock_data(e):
        symbol = stock_symbol.current.value.upper().strip()
        time_range = time_range_dropdown.current.value or "30 days"
        days = get_days_for_range(time_range)

    if not symbol:
        error_messages.current.content = ft.Text("Please enter stock system")
        error_messages.current.visible = True 
        price_info.current.visible = False 
        price_text_below.current.visible = False
        chart_container.current.visible = False 
        page.update()
        return 

    error_messages.current.visible = False 
    error_messages.current.content = ft.Text("",color = ft.Colors.RED, size=14)

    loading_text = ft.Text("Loading Stock Data....", size=16,color = ft.Colors.BLUE)
    chart_container.current.content = loading_text
    chart_container.current.visible = True
    page.update()

    try:
        url:f""
        response = requests.get(url)
        data = response.json()

        time_series = data ["Time series (daily)"]

        dates = sorted(time_series.keys(), reverse=TRUE) [:days]
        dates.reverse()

        opens, highs, lows, closes = [], [], [], []

        for date in dates: 
            day_data = time_seriesp[date]
            open_price = float(day_data ["1. open"])
            high_price = float(day_data["2. high"])
            low_price = float(day_data["3. low"])
            close_price float(day_data["3. low"])
                
            opens.append(open_price)
            highs.append(high_price)
            lows.append(low_price)
            closes.append(close_price)

            lastest_data = sorted(time_series.keys(), reverse=True)[0]
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
            ], spacing=10) 
        ])

            price_info.current.visible = True 

            chart = ft.LineChartData(
                data points=[
                    ft.LineChartDataPoint(i, closes[i])
                    for i in range(len(closes))
                ], 
                stroke_width=3
                color=ft.Colors.ORANGE,
                below_line_bgcolor=ft.Colors.ORANGE_100,
            ),
        ,
        (
            border=ft.Border(
                bottom=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)),
                left=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)),
                top=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)),
                right=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE)),
            ),
            left_axis=ft.ChartAxis(
                labels_size=50,
            ),
            bottom_axis=ft.ChartAxis(
                labels_size=40,
                labels_interval=max(1, len(closes)//10),   
            ),
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY)
            min_y=min(closes)*0.95,
            max_y=max(closes)*1.05,
            min_x=0,
            max_x=max(closes)-1,
            expand=True

        )
        chart_container.current.content = ft.Container(
            content=ft.Column([
                ft.Text(f"Closing Prices - {get_range_label(time_range)} ({symbol})", size=18)
            ]. spacing=10),
            padding=20,
            border=ft.border.all(2, ft.Colors.GREY_300),
            border_radius=10
        )
        chart_container.current.visible=True

        price_text_below.current.content = ft.Text(
            f"Open: ${float(lastest_data['1. open']):.2f}" | "
            f"High: ${float(lastest_data['2. high']):.2f}" | "
            f"Low: ${float(lastest_data['3. low']):.2f}" | "
            f"Close: ${float(lastest_data['4. close']):.2f}" | ",
            size=16
            weight=ft.FontWeight.BOLD, 
            text_align=ft.TextAlign.CENTER

        )
        price_text_below.current.visible=True 

    except Exception as e:
        error_messages.current.content = ft.Text("Error fetching data....", color=ft.Colors.RED, size=14)
        error_messages.current.visible = True
        price_info.current.visible = False
        price_text_below.current.visible = False
        chart_container.current.visible = False
    page.update()

    #UI Layout

page.add (
    ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("Gotcha Stock App on Code with Josh"),
                ft.Text("Enter a Stock Symbol to view the chart...")
            ], spacings=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            paddings=ft.padding.only(bottom=20),
            alignment=ft.alignment.center 
),

ft.Container(
    content=ft.Row([
    ft.TextField(
        ref=stock_symbol, 
        label="Stock Symbol",
        hint_text= "APPL, GOOGL, MSFT"
        width=300,
        autofocus=True,
        on_submit=fetch_stock_data,
    ),
                ft.Dropdown(
                    ref=time_range_dropdown,
                    label="Time Range",
                    width=150,
                    options=[
                        ft.dropdown.Option("1 week"),
                        ft.dropdown.Option("2 weeks"),
                        ft.dropdown.Option("30 days"),
                        ft.dropdown.Option("90 days"),
                        ft.dropdown.Option("1 years"),
                        ft.dropdown.Option("5 years"),
                    ],
                    value="30 days"

                ),
                ft.ElevatedButton(
                    "Get Stock Data",
                    icon=ft.Icons.SEARCH,
                    on_click=fetch_stock_data,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_700.
                    ),
                ),
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        )   ),
            alignment=ft.alignment.center
),
ft.Container(
    ref=error_messages,
    content=ft.Text(""),
    padding=10,
    visible=False
),
ft.Container(
    ref=price_info,
    padding=10,
    visible=False
),
ft.Container(
    ref=chart_container
    padding=10
    visible=False
),
ft.Container(
    ref=price_text_below,
    padding=10,
    visible=False
),
, spacing=15)


if __name__ = "__main__":
ft.app(target=main)