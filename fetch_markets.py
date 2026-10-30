#!/usr/bin/env python3
"""Récupère les dernières clôtures des indices et des valeurs tech suivis (Yahoo Finance).

Affiche un JSON {"indices": [...], "stocks": [...]} à recopier dans le bloc `markets`
de l'édition du jour. Un symbole introuvable est simplement omis.
Régénère aussi `market_history.js`, l'historique sur 5 ans affiché dans le graphique.
"""
import json
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

INDICES = [
    ("^IXIC", "Nasdaq Composite", "US"),
    ("^NDX", "Nasdaq 100", "US"),
    ("^GSPC", "S&P 500", "US"),
    ("^DJI", "Dow Jones", "US"),
    ("^VIX", "VIX (peur)", "US"),
    ("^FCHI", "CAC 40", "Europe"),
    ("^GDAXI", "DAX", "Europe"),
    ("^STOXX50E", "Euro Stoxx 50", "Europe"),
    ("^N225", "Nikkei 225", "Asie"),
    ("^HSI", "Hang Seng", "Asie"),
]

STOCKS = [
    ("NVDA", "Nvidia"),
    ("AAPL", "Apple"),
    ("MSFT", "Microsoft"),
    ("GOOGL", "Alphabet"),
    ("AMZN", "Amazon"),
    ("META", "Meta"),
    ("TSLA", "Tesla"),
]

# Séries des graphiques. Noms repris tels quels par les sous-onglets de la page (MARKET_REGIONS dans index.html).
CHART_SERIES = [
    ("^IXIC", "Nasdaq"),
    ("^GSPC", "S&P 500"),
    ("^DJI", "Dow Jones"),
    ("^FCHI", "CAC 40"),
    ("^GDAXI", "DAX"),
    ("^STOXX50E", "Euro Stoxx 50"),
    ("^N225", "Nikkei 225"),
    ("^HSI", "Hang Seng"),
    ("EEM", "Marchés émergents"),
]

SITE_DIR = Path(__file__).resolve().parent

USER_AGENT = "Mozilla/5.0"


def fetch_sessions(symbol, period):
    """Renvoie la liste des séances clôturées [(date ISO, clôture)], ou [] en cas d'échec."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(symbol)}?range={period}&interval=1d"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            result = json.load(response)["chart"]["result"][0]
    except Exception as error:
        print(f"{symbol} ignoré : {error}", file=sys.stderr)
        return []

    timestamps = result.get("timestamp") or []
    closes = result["indicators"]["quote"][0].get("close") or []
    sessions = [(ts, close) for ts, close in zip(timestamps, closes) if close is not None]
    # Séance encore ouverte : on l'écarte pour ne garder que des cours de clôture.
    trading_period = result["meta"].get("currentTradingPeriod", {}).get("regular", {})
    if sessions and trading_period and sessions[-1][0] >= trading_period["start"] and time.time() < trading_period["end"]:
        sessions.pop()
    # Date de séance à l'heure de la place (Tokyo ouvre la veille en heure UTC).
    utc_offset = timedelta(seconds=result["meta"].get("gmtoffset", 0))
    return [
        ((datetime.fromtimestamp(ts, timezone.utc) + utc_offset).date().isoformat(), close)
        for ts, close in sessions
    ]


def fetch_last_close(symbol):
    """Renvoie (dernière clôture, variation en %, date de séance) ou None."""
    sessions = fetch_sessions(symbol, "10d")
    if len(sessions) < 2:
        print(f"{symbol} ignoré : pas assez de séances", file=sys.stderr)
        return None
    (_, previous_close), (session_date, last_close) = sessions[-2], sessions[-1]
    change_pct = (last_close - previous_close) / previous_close * 100
    return round(last_close, 2), round(change_pct, 2), session_date


def collect(entries, build):
    rows = []
    for entry in entries:
        quote_data = fetch_last_close(entry[0])
        if quote_data:
            rows.append(build(entry, *quote_data))
    return rows


def write_chart_history():
    """Écrit market_history.js : dates communes et clôtures alignées de chaque série.

    Les places n'ont pas les mêmes jours fériés : un jour sans séance reprend la clôture
    précédente. Si une série échoue, l'ancien fichier est conservé.
    """
    histories = {}
    for symbol, name in CHART_SERIES:
        sessions = fetch_sessions(symbol, "5y")
        if not sessions:
            print("market_history.js non mis à jour", file=sys.stderr)
            return
        histories[name] = dict(sessions)

    dates = sorted(set().union(*histories.values()))
    series = []
    for name, closes_by_date in histories.items():
        closes, last_close = [], None
        for day in dates:
            last_close = closes_by_date.get(day, last_close)
            closes.append(round(last_close, 2) if last_close is not None else None)
        series.append({"name": name, "closes": closes})

    history = {"dates": dates, "series": series}
    (SITE_DIR / "market_history.js").write_text(
        "window.MARKET_HISTORY = " + json.dumps(history, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )


indices = collect(INDICES, lambda e, value, pct, day: {
    "name": e[1], "region": e[2], "value": value, "changePct": pct, "session": day,
})
stocks = collect(STOCKS, lambda e, value, pct, day: {
    "ticker": e[0], "name": e[1], "value": value, "changePct": pct, "session": day,
})
write_chart_history()

print(json.dumps({"indices": indices, "stocks": stocks}, ensure_ascii=False, indent=1))
