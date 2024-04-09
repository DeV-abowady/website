

const chartProperties = {
  width:850,
  height:600,
  layout: {

    timeScale:{
      timeVisible:true,
      secondsVisible:false,
    }
}
}
const domElement = document.getElementById('tvchart');
const chart = LightweightCharts.createChart(domElement,chartProperties);
const candleSeries = chart.addCandlestickSeries();


function charte(symbol,timeframe){
  fetch("https://api.binance.com/api/v3/klines?symbol="+symbol+"&interval="+timeframe+"&limit=1000")
    .then(res => res.json())
    .then(data => {
      const cdata = data.map(d => {
        return {time:d[0]/1000,open:parseFloat(d[1]),high:parseFloat(d[2]),low:parseFloat(d[3]),close:parseFloat(d[4])}
      });
      candleSeries.setData(cdata);
    })
    .catch(err => log(err))
  }


function getTimeframe(clickedElement) {
  // Get the inner HTML value of the clicked li element
  const timeframeValue = clickedElement.innerHTML;
  let catl = document.getElementById('symbol').value;
  // Process or display the timeframe value here (e.g., console.log, send to server)
  console.log("current timeframe:", timeframeValue);
  charte(catl,timeframeValue)

  // Update the element with ID "text"
  const textElement = document.getElementById('text');
  if (textElement) { 
    textElement.innerHTML = catl + " Chart (" + timeframeValue + ")";
  } else {
    console.error("Element with ID 'text' not found.");
  }
  
}
 


let catl = document.getElementById('symbol');
if (catl.value == "BTCUSDT" ) {
    let text = document.getElementById('text').innerHTML = catl.value+" Chart "+ "(1h)" 

    charte(catl.value,"1h")
    
}


catl.onblur=function(){
    let text = document.getElementById('text').innerHTML =catl.value+" Chart"+ "(1h)" 
    console.log(catl.value)
    charte(catl.value,"1h")
  }


function upperCase() {
    const x = document.getElementById("symbol");
    x.value = x.value.toUpperCase();
  }


const amountInput = document.getElementById('Amount');
const amountLabel = document.getElementById('AmountLabel'); 
const hideAmountCheckbox = document.getElementById('hideAmount');
  
hideAmountCheckbox.addEventListener('change', () => {
    
    const isChecked = hideAmountCheckbox.checked;
  
    amountInput.hidden = isChecked;
    amountLabel.hidden = isChecked; // Hide the label too
  
    // Optional: Set placeholder text based on checkbox state
    // amountInput.placeholder = isChecked ? 'Amount Hidden' : 'Enter Amount';
  });
  
  // Initial State (Optional): If you want the amount hidden by default
if (hideAmountCheckbox.checked) {
    amountInput.hidden = true;
    amountLabel.hidden = true;

  }