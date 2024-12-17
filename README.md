# Stock Screen

A dynamic stock ticker display for OBS/Streamlabs browser sources, allowing live updates and customizable tickers.

---

## Features

- **Open Source**: Completely free using the MIT license, donate if you want.
- **Live Stock Updates**: Fetch real-time stock prices with smooth scrolling updates.
- **Customizable Tickers**: Easily modify tickers through the included GUI.
- **Company Logos**: Automatically fetch and display company logos for a clean, professional look.
- **OBS-Friendly Presets**: CSS styling presets for transparent and background-based displays.

---

## OBS/Streamlabs-Friendly CSS Presets 🎨  

To use these presets, simply apply the following CSS to your OBS/Streamlabs Browser Source settings:

1. **Transparent Background with White Text**  
   ```css
   body { background-color: rgba(0, 0, 0, 0); color: white; margin: 0px; overflow: hidden; }
   ```

2. **Transparent Background with Black Text**  
   ```css
   body { background-color: rgba(0, 0, 0, 0); color: black; margin: 0px; overflow: hidden; }
   ```

3. **White Background with Black Text**  
   ```css
   body { background-color: white; color: black; margin: 0px; overflow: hidden; }
   ```

4. **Black Background with White Text**  
   ```css
   body { background-color: black; color: white; margin: 0px; overflow: hidden; }
   ```

---

## How to Run

1. **Dependencies**: Ensure Python and required libraries are installed.  
2. Clone the repository:
   ```bash
   git clone https://github.com/m0rse-dab/StockScreen.git
   cd StockScreen
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the program:
   ```bash
   python main.py
   ```
5. Open the browser window at `http://localhost:8000/stock_ticker.html` to view the stock ticker.

---

## Support My Work ☕  

If you find this tool useful, consider supporting me on [Ko-fi](https://ko-fi.com/m0rse). Your support helps me keep developing tools like this!  

[![Ko-fi](https://img.shields.io/badge/Support%20Me-Ko--fi-FF5E5B?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ko-fi.com/your-kofi-link)

---

## License

This project is licensed under the MIT License.
