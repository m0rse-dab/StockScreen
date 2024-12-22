# StockScreen

A dynamic stock ticker display for OBS/Streamlabs browser sources, allowing live updates and customizable tickers.  
Since it's just HTML outputted, it can be used in numerous ways and repurposed for other projects.

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

### 1. Transparent Background with White Text

```css
body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background-color: transparent;
    overflow: hidden;
    display: flex;
    align-items: center;
    height: 100vh;
}

.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background-color: transparent;
    position: relative;
}

.ticker {
    display: flex;
    width: max-content;
    animation: scroll 20s linear infinite;
    white-space: nowrap;
}

.ticker:hover {
    animation-play-state: paused;
}

@keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

.stock {
    display: inline-block;
    padding: 12px 15px;
    font-size: 16px;
    color: #fff;
    border-radius: 8px;
    background-color: transparent;
    margin-right: 30px;
    transition: background-color 0.3s ease;
}

.stock:hover {
    background-color: rgba(0, 0, 0, 0.1);
}

.green {
    color: #2ecc71;
    font-weight: 600;
}

.red {
    color: #e74c3c;
    font-weight: 600;
}

.logo {
    height: 28px;
    width: 28px;
    margin-right: 12px;
    vertical-align: middle;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid rgba(0, 0, 0, 0.1);
}

strong {
    font-weight: 600;
    letter-spacing: -0.5px;
}
```

### 2. Black Background with White Text

```css
body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background-color: black;
    color: white;
    overflow: hidden;
    display: flex;
    align-items: center;
    height: 100vh;
}

.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background-color: black;
    position: relative;
}

.ticker {
    display: flex;
    width: max-content;
    animation: scroll 20s linear infinite;
    white-space: nowrap;
}

.ticker:hover {
    animation-play-state: paused;
}

@keyframes scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

.stock {
    display: inline-block;
    padding: 12px 15px;
    font-size: 16px;
    color: #fff;
    border-radius: 8px;
    background-color: transparent;
    margin-right: 30px;
    transition: background-color 0.3s ease;
}

.stock:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.green {
    color: #2ecc71;
    font-weight: 600;
}

.red {
    color: #e74c3c;
    font-weight: 600;
}

.logo {
    height: 28px;
    width: 28px;
    margin-right: 12px;
    vertical-align: middle;
    border-radius: 50%;
    object-fit: cover;
    border: 1px solid rgba(0, 0, 0, 0.1);
}

strong {
    font-weight: 600;
    letter-spacing: -0.5px;
}
```

---

## How to Run

### Windows:
1. Unzip the release version somewhere.
2. Run the executable.

### Other systems:
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
