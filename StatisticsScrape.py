import os
import requests
from yfinance import Ticker
import pandas as pd
import tkinter as tk
from bs4 import BeautifulSoup as bs

#"\python.exe" -m PyInstaller --onefile StatisticsScrape.py --windowed

old_stock_csv_filepath = "stock_info.csv"

stock_ticker_list = ["O", "MSFT", "AAPL", "ASML", "SYK", "DHR", "TMO", "UNH", "JNJ", "COST", "NKE", "LVMHF",
                     "HD", "LOW", "BLK", "MA", "MSCI", "SPGI", "V", "DE", "UNP", "VICI", "AWK", "SNA",
                     "SBUX", "LIN", "GOOG", "GOOGL" ]


def create_popup(pop_text):
    # Create the main window
    root = tk.Tk()
    root.title("Dividend Increases")

    # Set the size of the pop-up window
    window_width = root.winfo_screenwidth() // 2
    window_height = root.winfo_screenheight() // 2
    root.geometry(f"{window_width}x{window_height}+{window_width // 2}+{window_height // 2}")

    # Increase font size
    font = ("Helvetica", 20)

    # Create a label with the custom text
    label = tk.Label(root, text=pop_text, font=font)
    label.pack(padx=20, pady=20)

    # Function to close the popup window
    def close_popup():
        root.destroy()

    # Button to close the popup window
    close_button = tk.Button(root, text="Close", font=font, command=close_popup)
    close_button.pack(pady=10)

    root.attributes("-topmost", True)

    # Run the Tkinter event loop
    root.mainloop()


def scrape_stock(ticker_symbol):
    dividend_yield = Ticker(ticker_symbol).info['dividendRate']
    stock = {"ticker": ticker_symbol, "dividendyield": dividend_yield}
    return stock


def compare_old_new_csv(comparison_csv):

    dividend_increases = {}
    dividend_decreases = {}

    for index, row in comparison_csv.iterrows():
        if row["dividendyield"] > row["olddividendyield"]:
            dividend_increases[row["ticker"]] = (row["dividendyield"] / row["olddividendyield"] - 1) * 100
        elif row["dividendyield"] < row["olddividendyield"]:
            dividend_decreases[row["ticker"]] = (row["olddividendyield"] / row["dividendyield"] - 1) * 100
    stock_csv.to_csv("stock_info.csv", index=False)

    return dividend_increases, dividend_decreases


def create_popup_text(dividend_increases, dividend_decreases):

    text = ""

    for key, value in dividend_increases.items():
        text += F"\n {key}: + {round(value, 2)}%"
    for key, value in dividend_decreases.items():
        text += F"\n {key}: - {round(value, 2)}%"

    return text


def prepare_old_csv():

    old_stock_csv = pd.read_csv(old_stock_csv_filepath, delimiter=",")

    old_stock_csv["olddividendyield"] = old_stock_csv["dividendyield"]

    old_stock_csv.drop(["dividendyield", "ticker"], axis=1, inplace=True)

    return old_stock_csv


stocks = []

# get dividend yield for all stocks
for ticker_symbol in stock_ticker_list:
    stocks.append(scrape_stock(ticker_symbol))

# create csv with stock info
stock_csv = pd.DataFrame(stocks)

# read in old stock info
old_csv = prepare_old_csv()

# compare dividend yield
comparison_csv = old_csv.join(stock_csv, how="inner")
dividend_increases, dividend_decreases = compare_old_new_csv(comparison_csv)

# create output text
popup_text = create_popup_text(dividend_increases, dividend_decreases)

create_popup(popup_text)
