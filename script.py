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
import webbrowser  # Added for opening the default browser

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

# Load tickers from JSON file if it exists
def load_tickers():
    global tickers
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                tickers = list(data.keys())
                print(f"Loaded tickers from {JSON_FILE}: {tickers}")
        except Exception as e:
            print(f"Error loading tickers from {JSON_FILE}: {e}")
    else:
        print("No JSON file found, using default tickers.")


load_tickers()

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

def start_server(stop_event):
    """Start a local HTTP server."""
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", SERVER_PORT), handler) as httpd:
        print(f"Serving at http://localhost:{SERVER_PORT}/{OUTPUT_FILE}")

        # Automatically open the browser
        webbrowser.open(f"http://localhost:{SERVER_PORT}/{OUTPUT_FILE}", new=2)

        # Serve until stop_event is set
        while not stop_event.is_set():
            httpd.handle_request()

def open_gui(stop_event):
    """GUI to manage tickers live."""
    global tickers

    def add_ticker():
        new_ticker = simpledialog.askstring("Input", "Enter ticker symbol:")
        if new_ticker:
            new_ticker = new_ticker.upper()
            if new_ticker not in tickers:
                tickers.append(new_ticker)
                refresh_list()
                messagebox.showinfo("Success", f"{new_ticker} added.")
            else:
                messagebox.showwarning("Warning", f"{new_ticker} already exists.")

    def remove_ticker():
        rem_ticker = simpledialog.askstring("Input", "Enter ticker to remove:")
        if rem_ticker and rem_ticker.upper() in tickers:
            tickers.remove(rem_ticker.upper())
            refresh_list()
            messagebox.showinfo("Success", f"{rem_ticker.upper()} removed.")
        else:
            messagebox.showwarning("Warning", f"{rem_ticker} not in list.")

    def refresh_list():
        for widget in frame.winfo_children():
            widget.destroy()
        tk.Label(frame, text="Stocks", font=("Arial", 12, "bold")).pack()
        for ticker in tickers:
            tk.Label(frame, text=ticker, font=("Arial", 10)).pack()

    def on_close():
        stop_event.set()
        root.destroy()
        print("GUI closed. Stopping server and exiting.")

    root = tk.Tk()
    root.title("Stock Ticker Manager")
    root.geometry("300x400")

    header = tk.Frame(root)
    header.pack(pady=10)

    tk.Button(header, text="Add", command=add_ticker).grid(row=0, column=0, padx=10)
    tk.Button(header, text="Remove", command=remove_ticker).grid(row=0, column=1, padx=10)
    try:
        refresh_icon = tk.PhotoImage(file="refresh_icon.png")  # Replace with a path to your refresh icon image
        tk.Button(header, image=refresh_icon, command=refresh_list).grid(row=0, column=2, padx=10)
    except tk.TclError:
        tk.Button(header, text="Refresh", command=refresh_list).grid(row=0, column=2, padx=10)

    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, pady=20)

    refresh_list()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    print("Starting stock ticker server...")

    stop_event = threading.Event()

    # Start the GUI in a thread
    threading.Thread(target=open_gui, args=(stop_event,), daemon=True).start()

    # Start a thread to periodically update stock data
    threading.Thread(target=lambda: [update_json() or time.sleep(UPDATE_INTERVAL) for _ in iter(int, 1)], daemon=True).start()

    # Start the local server
    start_server(stop_event)
