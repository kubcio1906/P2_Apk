from views import fetch_and_save_commodity_data,fetch_and_save_fx_data,fetch_and_save_inflation_data,fetch_and_save_interest_rates_data,fetch_and_save_stock_data,data_exists_in_database
import requests
def auto_fetch_currency_data(api_key):
   
    base_currencies = ["EUR","USD","CHF"] #, "EUR", "CHF", "GBP"
    target_currencies = ["PLN"] #, "EUR", "CHF", "GBP"

    for base_currency in base_currencies:
        for target_currency in target_currencies:
            if base_currency != target_currency:
                symbol = base_currency + target_currency
                fetch_and_save_fx_data(symbol, api_key)
def auto_fetch_commodity_data(api_key):
    
    commodities = ["BRENT", "NATURAL_GAS", "COPPER", "COFFEE"]

    for commodity in commodities:
        fetch_and_save_commodity_data(commodity,api_key)
def auto_fetch_stock_data(api_key):
 
    # Lista symboli 10 najpopularniejszych spółek
    stock_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "FB", "TSLA", "BRK.A", "V", "JNJ", "WMT","NVDA"]

    for symbol in stock_symbols:
        fetch_and_save_stock_data(symbol,api_key)

def auto_fetch_inflation_data(api_key):
    
    fetch_and_save_inflation_data(api_key)

def auto_fetch_save_interest_rates_data(api_key):
    
    fetch_and_save_interest_rates_data(api_key)
