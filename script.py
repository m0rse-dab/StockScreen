import json
import yfinance as yf
import time
import os
import requests
import threading
import http.server
import socketserver
import tkinter as tk
from tkinter import simpledialog, messagebox

# CONFIGURATION
OUTPUT_FILE = "index.html"  # HTML output file
JSON_FILE = "stock_data.json"  # Stock data JSON file
LOGO_DIR = "logos"  # Directory to store company logos
UPDATE_INTERVAL = 30  # Interval to refresh stock data in seconds
SERVER_PORT = 8000  # Port for the local server
LOGO_URL_TEMPLATE = "https://logo.clearbit.com/{domain}"

# Default tickers
tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "RKLB"]

# Ensure necessary directories exist
if not os.path.exists(LOGO_DIR):
    os.makedirs(LOGO_DIR)


def get_stock_data(symbols):
    """Fetch stock data using yfinance."""
    stock_data = {}
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="5d")
            valid_closes = data['Close'].dropna()

            if len(valid_closes) >= 2:
                current_price = valid_closes.iloc[-1]
                prev_close = valid_closes.iloc[-2]
                price_change = current_price - prev_close
                percent_change = (price_change / prev_close) * 100
                stock_data[symbol] = (current_price, price_change, percent_change)
            else:
                stock_data[symbol] = (None, None, None)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            stock_data[symbol] = (None, None, None)
    return stock_data


def get_company_domain(symbol):
    """Fetch company domain for Clearbit logo API."""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        if "website" in info and info["website"]:
            return info["website"].replace("http://", "").replace("https://", "").replace("www.", "")
    except Exception as e:
        print(f"Error fetching domain for {symbol}: {e}")
    return f"{symbol.lower()}.com"


def download_logo(symbol):
    """Download and save company logos."""
    domain = get_company_domain(symbol)
    logo_url = LOGO_URL_TEMPLATE.format(domain=domain)
    logo_path = os.path.join(LOGO_DIR, f"{symbol}.png")

    if not os.path.exists(logo_path):  # Download only if not already existing
        try:
            response = requests.get(logo_url, timeout=5)
            if response.status_code == 200:
                with open(logo_path, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded logo for {symbol}")
            else:
                print(f"Failed to download logo for {symbol}: Status {response.status_code}")
        except Exception as e:
            print(f"Error downloading logo for {symbol}: {e}")
    return logo_path


def update_json():
    """Save stock data into a JSON file and download logos."""
    stock_data = get_stock_data(tickers)
    enhanced_data = {}

    for symbol, data in stock_data.items():
        logo_path = download_logo(symbol)
        enhanced_data[symbol] = {"data": data, "logo": logo_path}

    with open(JSON_FILE, "w", encoding="utf-8") as json_file:
        json.dump(enhanced_data, json_file)
    print("Updated stock data and logos.")


def start_server():
    """Start a local HTTP server."""
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", SERVER_PORT), handler) as httpd:
        print(f"Serving at http://localhost:{SERVER_PORT}/{OUTPUT_FILE}")
        httpd.serve_forever()


def open_gui():
    """GUI to manage tickers live."""
    global tickers

    def add_ticker():
        new_ticker = simpledialog.askstring("Input", "Enter ticker symbol:")
        if new_ticker:
            new_ticker = new_ticker.upper()
            if new_ticker not in tickers:
                tickers.append(new_ticker)
                messagebox.showinfo("Success", f"{new_ticker} added.")
            else:
                messagebox.showwarning("Warning", f"{new_ticker} already exists.")

    def remove_ticker():
        rem_ticker = simpledialog.askstring("Input", "Enter ticker to remove:")
        if rem_ticker and rem_ticker.upper() in tickers:
            tickers.remove(rem_ticker.upper())
            messagebox.showinfo("Success", f"{rem_ticker.upper()} removed.")
        else:
            messagebox.showwarning("Warning", f"{rem_ticker} not in list.")

    def show_tickers():
        messagebox.showinfo("Current Tickers", "\n".join(tickers))

    root = tk.Tk()
    root.title("Stock Ticker Manager")
    root.geometry("300x200")

    tk.Button(root, text="Add Ticker", command=add_ticker, width=20).pack(pady=5)
    tk.Button(root, text="Remove Ticker", command=remove_ticker, width=20).pack(pady=5)
    tk.Button(root, text="Show Tickers", command=show_tickers, width=20).pack(pady=5)
    tk.Button(root, text="Update Data", command=update_json, width=20).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    print("Starting stock ticker server...")
    threading.Thread(target=open_gui, daemon=True).start()  # Launch the GUI in a thread
    update_json()

    # Start a thread to periodically update stock data
    threading.Thread(target=lambda: [update_json() or time.sleep(UPDATE_INTERVAL) for _ in iter(int, 1)], daemon=True).start()

    # Start the local server
    start_server()

