from extensions import db
from models import CurrencyData, CommodityData, StockData,CPI_Data, InterestRateData
from datetime import datetime
import requests
from validators import (
    validate_stock_data_structure, validate_currency_data_structure, validate_commodity_data_structure,
    validate_cpi_data_structure, validate_interest_rates_data_structure
)
from services import(
auto_fetch_currency_data, auto_fetch_commodity_data,auto_fetch_inflation_data,auto_fetch_save_interest_rates_data,auto_fetch_stock_data
)
import numpy as np
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Funkcja do pobierania i zapisywania danych walutowych
def fetch_and_save_fx_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&outputsize=full&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        fx_data = response.json()

        is_valid, message = validate_currency_data_structure(fx_data)
        if not is_valid:
            return message

        if 'Time Series FX (Daily)' not in fx_data:
            return f"Key 'Time Series FX (Daily)' not found in API response for symbol {symbol}."

        for date_str, daily_data in fx_data['Time Series FX (Daily)'].items():
            # Obsługa brakujących danych
            if any(value is None for value in daily_data.values()):
                continue

            try:
                open_price = max(0, float(daily_data['1. open']))
                high_price = max(0, float(daily_data['2. high']))
                low_price = max(0, float(daily_data['3. low']))
                close_price = max(0, float(daily_data['4. close']))

                # Transformacja danych
                average_price = (open_price + high_price + low_price + close_price) / 4
                average_price = np.log(average_price + 1)

                # Weryfikacja poprawności danych
                if average_price < 0:
                    logging.warning(f"Nierealistyczna średnia cena dla daty {date_str}")
                    continue

                existing_entry = db.session.query(CurrencyData).filter(
                    CurrencyData.date == datetime.strptime(date_str, '%Y-%m-%d').date(),
                    CurrencyData.symbol == symbol
                ).first()

                if existing_entry is None:
                    new_entry = CurrencyData(
                        symbol=symbol,
                        date=datetime.strptime(date_str, '%Y-%m-%d').date(),
                        open_price=open_price,
                        high_price=high_price,
                        low_price=low_price,
                        close_price=close_price,
                        average_price=average_price
                    )
                    db.session.add(new_entry)
            except ValueError as e:
                logging.error(f"Błąd konwersji danych walutowych dla daty {date_str}: {e}")
                continue

        db.session.commit()
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid JSON response from API."
        
# Funkcja do pobierania i zapisywania danych o towarach
def fetch_and_save_commodity_data(name, api_key):
    url = f'https://www.alphavantage.co/query?function={name}&interval=daily&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        commodity_data = response.json()

        is_valid, message = validate_commodity_data_structure(commodity_data)
        if not is_valid:
            return message

        if 'data' not in commodity_data:
            return "Expected key 'data' not found in the JSON response."

        for data_point in commodity_data['data']:
            try:
                if 'value' not in data_point or data_point['value'] is None:
                    continue

                value_str = data_point['value']
                if isinstance(value_str, str):
                    value_str = value_str.replace(',', '.')
                price = float(value_str)

                existing_entry = db.session.query(CommodityData).filter(
                    CommodityData.date == datetime.strptime(data_point['date'], '%Y-%m-%d').date(),
                    CommodityData.name == name
                ).first()

                if existing_entry is None:
                    new_commodity = CommodityData(
                        name=name,
                        date=datetime.strptime(data_point['date'], '%Y-%m-%d').date(),
                        price=price,
                        unit=commodity_data.get('unit', 'not provided')
                    )
                    db.session.add(new_commodity)
            except ValueError as e:
                logging.error(f"Błąd konwersji danych towarowych dla daty {data_point['date']}: {e}")
                continue

        db.session.commit()
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid JSON response from API."

       
# Funkcja do pobierania i zapisywania danych akcji
def fetch_and_save_stock_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        stock_data_json = response.json()
        
        is_valid, message = validate_stock_data_structure(stock_data_json)
        if not is_valid:
            return message

        if 'Time Series (Daily)' not in stock_data_json:
            return "Expected key 'Time Series (Daily)' not found in the JSON response."

        for date_str, daily_data in stock_data_json['Time Series (Daily)'].items():
            if any(value is None for value in daily_data.values()):
                continue

            try:
                open_price = float(daily_data['1. open'])
                high_price = float(daily_data['2. high'])
                low_price = float(daily_data['3. low'])
                close_price = float(daily_data['4. close'])
                average_price = round((open_price + high_price + low_price + close_price) / 4, 2)
                volume = int(daily_data['5. volume'])

                existing_entry = db.session.query(StockData).filter(
                    StockData.date == datetime.strptime(date_str, '%Y-%m-%d').date(),
                    StockData.symbol == symbol
                ).first()

                if existing_entry is None:
                    new_entry = StockData(
                        symbol=symbol,
                        date=datetime.strptime(date_str, '%Y-%m-%d').date(),
                        average_price=average_price,
                        volume=volume
                    )
                    db.session.add(new_entry)
            except ValueError as e:
                logging.error(f"Błąd konwersji danych akcji dla daty {date_str}: {e}")
                continue

        db.session.commit()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {e}")
        return f"Request Exception: {e}"
    except ValueError as e:
        logging.error(f"Invalid JSON response from API: {e}")
        return "Invalid JSON response from API."

# Funkcja do pobierania i zapisywania danych o inflacji
def fetch_and_save_inflation_data(api_key):
    url = f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        inflation_data = response.json()

        is_valid, message = validate_cpi_data_structure(inflation_data)
        if not is_valid:
            return message

        if 'data' not in inflation_data:
            return "Key 'data' not found in API response."

        for data_point in inflation_data['data']:
            try:
            # Obsługa brakujących danych
                if 'value' not in data_point or data_point['value'] is None:
                    continue
                date = datetime.strptime(data_point['date'], '%Y-%m-%d').date()
                value = float(data_point['value'])

                existing_entry = db.session.query(CPI_Data).filter(CPI_Data.date == date).first()

                if existing_entry is None:
                    new_cpi_data = CPI_Data(date=date, value=value)
                    db.session.add(new_cpi_data)
            except ValueError as e:
                logging.error(f"Błąd konwersji danych towarowych dla daty {data_point['date']}: {e}")
                continue

        db.session.commit()
        return "CPI data fetched and saved successfully."
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid JSON response from API."
    
# Funkcja do pobierania i zapisywania danych o stopach procentowych
def fetch_and_save_interest_rates_data(api_key):
    url = f'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        interest_rates_data = response.json()

        is_valid, message = validate_interest_rates_data_structure(interest_rates_data)
        if not is_valid:
            return message

        if 'data' not in interest_rates_data:
            return "Key 'data' not found in API response."

        for data_point in interest_rates_data['data']:
            try:
                
                if 'value' not in data_point or data_point['value'] is None:
                    continue
                date = datetime.strptime(data_point['date'], '%Y-%m-%d').date()
                value = float(data_point['value'])

                existing_entry = db.session.query(InterestRateData).filter(
                    InterestRateData.date == date
                ).first()

                if existing_entry is None:
                    new_interest_rates_data = InterestRateData(
                        date=date, 
                        value=value
                    )
                    db.session.add(new_interest_rates_data)
            except ValueError:
                print(f"Błąd konwersji danych stóp procentowych dla daty {data_point['date']}")
                continue

        db.session.commit()
        return "Interest rates data fetched and saved successfully."
    except requests.exceptions.RequestException as e:
        return f"Request Exception: {e}"
    except ValueError:
        return "Invalid JSON response from API."
    
# Funkcja sprawdzająca, czy dane już istnieją w bazie danych
def data_exists_in_database(data_type, date):
    date = datetime.strptime(date, '%Y-%m-%d').date()  
   
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
    
   

