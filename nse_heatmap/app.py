from flask import Flask, render_template, jsonify
import requests
import time

app = Flask(__name__)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
})

def refresh_cookies():
    try:
        session.get("https://www.nseindia.com/", timeout=10)
        time.sleep(0.5)
    except Exception as e:
        print(f"Cookie refresh failed: {e}")

def fetch_data(index):
    if index == "NIFTY50":
        # flag=1 returns all 50 stocks sorted by contribution
        url = "https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getContributionData&&index=NIFTY%2050&&noofrecords=0&&flag=1"
    else:
        # flag=1 returns ALL Bank Nifty stocks (not just top 5 contributors)
        url = "https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getContributionData&&index=NIFTY%20BANK&&noofrecords=0&&flag=1"

    for attempt in range(2):
        try:
            resp = session.get(url, timeout=10)
            if resp.status_code in (401, 403) or not resp.text.startswith("{"):
                print(f"Bad response {resp.status_code}, refreshing cookies...")
                refresh_cookies()
                continue
            data = resp.json().get("data", [])
            print(f"[{index}] Fetched {len(data)} stocks")
            return data
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            refresh_cookies()
    return []

def summarize(data):
    return {
        "data": data,
        "green": sum(1 for d in data if d.get("isPositive") == "Y"),
        "red":   sum(1 for d in data if d.get("isPositive") == "N"),
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/data/<index_name>")
def get_data(index_name):
    return jsonify(summarize(fetch_data(index_name)))

@app.route("/api/both")
def get_both():
    nifty = fetch_data("NIFTY50")
    bank  = fetch_data("BANKNIFTY")
    return jsonify({"nifty": summarize(nifty), "bank": summarize(bank)})

if __name__ == "__main__":
    refresh_cookies()
    app.run(debug=True, port=5000)
