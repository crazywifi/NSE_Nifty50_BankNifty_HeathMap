# NSE Heatmap

A web-based heatmap for NIFTY 50 and BANK NIFTY with auto-refresh.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 in your browser.

## Features
- Toggle between NIFTY 50 and BANK NIFTY heatmaps
- Green/Red count badges
- Auto-refresh: 1min, 2min, or custom interval
- Automatic cookie refresh (hits NSE homepage to get fresh cookies)
- Color-coded cells with price and % change

## Notes
- NSE uses Akamai bot protection, so occasionally requests may fail.
  The app will retry on the next interval automatically.
- Run during market hours (9:15 AM – 3:30 PM IST) for live data.
