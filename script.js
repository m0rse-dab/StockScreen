async function loadStockData() {
    const response = await fetch('/stock_data.json');
    const data = await response.json();
    const tickerDiv = document.querySelector('.ticker');
    tickerDiv.innerHTML = ''; // Clear previous content

    let tickerContent = '';

    // Populate ticker data
    for (const [symbol, value] of Object.entries(data)) {
        const [price, change, percent] = value.data;
        const colorClass = change > 0 ? 'green' : 'red';
        const sign = change > 0 ? '+' : '';
        const logo = value.logo;

        tickerContent += `
            <div class='stock'>
                <img class='logo' src='${logo}' alt='${symbol}' />
                ${symbol}: ${price !== null ? price.toFixed(2) : 'N/A'}
                <span class='${colorClass}'>${sign}${change?.toFixed(2)} (${sign}${percent?.toFixed(2)}%)</span>
            </div>`;
    }

    // Repeat ticker content to ensure seamless scrolling
    tickerDiv.innerHTML = tickerContent + tickerContent;
}

setInterval(loadStockData, 5000);
window.onload = loadStockData;

