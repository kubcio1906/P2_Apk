from extensions import db
from models import CurrencyData, CommodityData, StockData,CPI_Data, InterestRateData
from datetime import datetime
import requests
from validators import (
    validate_stock_data_structure, validate_currency_data_structure, validate_commodity_data_structure,
    validate_cpi_data_structure, validate_interest_rates_data_structure
)

def fetch_and_save_fx_data(symbol,api_key):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&outputsize=full&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        fx_data = response.json()
    
         # Walidacja struktury danych
        is_valid, message = validate_currency_data_structure(fx_data)
        if not is_valid:
            return message  # Zwraca komunikat o błędzie, jeśli dane są niepoprawne


       
        if 'Time Series FX (Daily)' not in fx_data:
            return f"Key 'Time Series FX (Daily)' not found in API response for symbol {symbol}."

        for date_str, daily_data in fx_data['Time Series FX (Daily)'].items():
            
            open_price = round(float(daily_data['1. open']),2)
            high_price = round(float(daily_data['2. high']),2)
            low_price = round(float(daily_data['3. low']),2)
            close_price = round(float(daily_data['4. close']),2)
            average_price = round((open_price + high_price + low_price + close_price) / 4 ,2)
                
            new_entry = CurrencyData(
                symbol=symbol,
                date=datetime.strptime(date_str, '%Y-%m-%d').date(),
                open_price=open_price,
                high_price=high_price,
                low_price=low_price,
                close_price=close_price,
                average_price=average_price  # obliczona średnia cena
                )
            db.session.add(new_entry)
        db.session.commit()
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Error: {err}"
    except ValueError:
        return "Invalid JSON response from API."
   
        

def fetch_and_save_commodity_data(name, api_key):
    
    url = f'https://www.alphavantage.co/query?function={name}&interval=daily&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        commodity_data = response.json()
        is_valid, message =  validate_commodity_data_structure(commodity_data)
        if not is_valid:
            return message  # Zwraca komunikat o błędzie, jeśli dane są niepoprawne
       
        if 'data' not in commodity_data:
            return "Expected key 'data' not found in the JSON response."
        for data_point in commodity_data['data']:
            # Sprawdzanie, czy wartość jest stringiem i zamiana przecinka na kropkę
            value_str = data_point['value']
            if isinstance(value_str, str):
                value_str = value_str.replace(',', '.')
            try:
                price = float(value_str)
            except ValueError:
                continue  # Przechodzi do następnego elementu, jeśli konwersja się nie powiedzie

            new_commodity = CommodityData(
                name=name,
                date=datetime.strptime(data_point['date'], '%Y-%m-%d').date(),
                price=price,
                unit=commodity_data.get('unit', 'not provided')
            )
            db.session.add(new_commodity)
        db.session.commit()
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid JSON response from API."
       

def fetch_and_save_stock_data(symbol,api_key):
   
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        stock_data_json = response.json()
         # Walidacja struktury danych
        is_valid, message = validate_stock_data_structure(stock_data_json)
        if not is_valid:
            return message  # Zwraca komunikat o błędzie, jeśli dane są niepoprawne
        if 'Time Series (Daily)' not in stock_data_json:
            return "Expected key 'Time Series (Daily)' not found in the JSON response."

        for date_str, daily_data in stock_data_json['Time Series (Daily)'].items():
            try:
                open_price = float(daily_data['1. open'])
                high_price = float(daily_data['2. high'])
                low_price = float(daily_data['3. low'])
                close_price = float(daily_data['4. close'])
                average_price =  round((open_price + high_price + low_price + close_price) / 4,2)
                volume = int(daily_data['5. volume'])
                    
                    
                new_entry = StockData(
                    symbol=symbol,
                    date=date_str,
                    average_price=average_price,
                    volume=volume
                )
                db.session.add(new_entry)
            except TypeError as e:
                    print(f"Błąd podczas przetwarzania danych: {e}")
                    print(f"Dane: {daily_data}")

            db.session.commit()
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid JSON response from API."

def fetch_and_save_inflation_data(api_key):
    url = f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        inflation_data = response.json()
        is_valid, message =  validate_cpi_data_structure(inflation_data)
        if not is_valid:
            return message  # Zwraca komunikat o błędzie, jeśli dane są niepoprawne
        if 'data' not in inflation_data:
            return f"Key 'data' not found in API response."
        
        for data_point in inflation_data['data']:
            date = datetime.strptime(data_point['date'], '%Y-%m-%d').date()
            value = float(data_point['value'])

            new_cpi_data = CPI_Data(date=date, value=value)
            db.session.add(new_cpi_data)
        db.session.commit()
        return "CPI data fetched and saved successfully."
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid JSON response from API."
    

def fetch_and_save_interest_rates_data(api_key):
    url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        interest_rates_data = response.json()
        is_valid, message =  validate_interest_rates_data_structure(interest_rates_data)
        if not is_valid:
            return message  # Zwraca komunikat o błędzie, jeśli dane są niepoprawne
        if 'data' not in interest_rates_data:
            return f"Key 'data' not found in API response."

        for data_point in interest_rates_data['data']:
            date = datetime.strptime(data_point['date'], '%Y-%m-%d').date()
            value = float(data_point['value'])

            new_interest_rates_data = InterestRateData(date=date, value=value)
            db.session.add(new_interest_rates_data)
        db.session.commit()
        return "Retail sales data fetched and saved successfully."
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid JSON response from API."
    

def data_exists_in_database(data_type, date):
    date = datetime.strptime(date, '%Y-%m-%d').date()  # Konwersja stringa na obiekt daty
   
    if data_type == 'currency_pairs':
        return db.session.query(CurrencyData).filter(CurrencyData.date == date).count() > 0
    elif data_type == 'commodity_data':
        return db.session.query(CommodityData).filter(CommodityData.date == date).count() > 0
    elif data_type == 'stock_data':
        return db.session.query(StockData).filter(StockData.date == date).count() > 0
    elif data_type == 'inflation_data':
        return db.session.query(CPI_Data).filter(CPI_Data.date == date).count() > 0
    elif data_type == 'interest_rates_data':
        return db.session.query(InterestRateData).filter(InterestRateData.date == date).count() > 0
    else:
        raise ValueError("Nieznany typ danych")

    return False
    
   
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

