#
#
# Script zur Abschätzung des Bitcoin-Preises nach dem PowerLaw-Modell
#
#
from datetime import datetime

# Funktion zur Berechnung des Bitcoin Power-Law Preises (Fair-Preis)
def bitcoin_power_law_price(days_since_genesis):
    # Power-Law-Formel: 1.0117e-17 * (days_since_genesis)^5.82
    price = 1.0117e-17 * (days_since_genesis ** 5.82)
    return price

# Funktion zur Schätzung des Bottom-Preises als Prozentsatz des Fair-Preises
def bitcoin_bottom_price(fair_price, percentage=0.355):
    bottom_price = fair_price * percentage  # Zum Beispiel 35.5% des Fair-Preises
    return bottom_price

# Funktion zur Schätzung des Top-Preises als Prozentsatz des Fair-Preises
def bitcoin_top_price(fair_price, percentage=5.16):
    top_price = fair_price * percentage  # Zum Beispiel 516% des Fair-Preises
    return top_price


def getval(j, m, d):   
    print("---")
    # Heutiges Datum oder ein zukünftiges Datum
    future_date = datetime.now()  # Kann angepasst werden
    future_date = datetime(2024, 9, 19);
    future_date = datetime(j, m, d);

 

    print("future_date: " ,future_date)

    # Berechne die Anzahl der Tage seit dem Genesis Block
    days_since_genesis = (future_date - genesis_block_date).days

    # Berechne den Bitcoin Fair Price
    fair_price = bitcoin_power_law_price(days_since_genesis)

    # Berechne den Bitcoin Bottom Price (z.B. 35.5% des Fair-Preises)
    bottom_price = bitcoin_bottom_price(fair_price, percentage=0.42)

    # Berechne den Bitcoin Top Price (z.B. 516% des Fair-Preises)
    #top_price = bitcoin_top_price(fair_price, percentage=5.16)
    top_price = bitcoin_top_price(fair_price, percentage=2.7)


    # Ausgabe
    BOLD = '\033[1m'
    END = '\033[0m'
    print(f"Tage seit dem Genesis Block: {days_since_genesis}")
    print(f"{BOLD}Bitcoin Fair Price: {fair_price:.2f} USD{END}")
    print(f"Bitcoin Bottom Price (42.0% des Fair-Preises): {bottom_price:.2f} USD")
    print(f"Bitcoin Top Price (270% des Fair-Preises): {top_price:.2f} USD")
    return fair_price



# Datum des Genesis Blocks: 3. Januar 2009
genesis_block_date = datetime(2009, 1, 3)


fp = getval(2024,9,19)
print("Ergebnis Fair Price: ",fp)
 

 