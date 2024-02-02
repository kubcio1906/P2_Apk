from extensions import db
from models import CurrencyData, CommodityData, StockData,CPI_Data, InterestRateData,TimeDimension,EmaData,RsiData,CorrelationData
from datetime import datetime , date , timedelta
import requests
from sqlalchemy import create_engine, select, update, extract
from validators import (
    validate_stock_data_structure, validate_currency_data_structure, validate_commodity_data_structure,
    validate_cpi_data_structure, validate_interest_rates_data_structure
)
import numpy as np
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, select, update, extract
import pandas as pd
from sqlalchemy.orm import sessionmaker
# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Funkcja do pobierania i zapisywania danych walutowych
def fetch_and_save_fx_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&outputsize=full&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        fx_data = response.json()
       
        logging.info(f"Odpowiedź API dla {symbol}: {fx_data}")
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

                
                existing_entry = db.session.query(CurrencyData).filter(
                CurrencyData.date == date_str,
                CurrencyData.symbol == symbol
                ).first()

                if existing_entry is None:
                    new_entry = CurrencyData(
                        symbol=symbol,
                        date=date_str,
                        open_price=open_price,
                        high_price=high_price,
                        low_price=low_price,
                        close_price=close_price,
                    
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
        

def fetch_and_save_commodity_data(name, api_key):
    url = f'https://www.alphavantage.co/query?function={name}&interval=monthly&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        commodity_data = response.json()
        #print(commodity_data)
        # Sprawdzenie, czy odpowiedź zawiera wymagane klucze
        if 'data' not in commodity_data:
            logging.error("Expected key 'data' not found in the JSON response.")
            return "Expected key 'data' not found in the JSON response."

        for date_str, data_point in commodity_data['data']:
            try:
                # Sprawdzenie, czy data_point zawiera wymagane pola
                if 'date' not in data_point or 'value' not in data_point or data_point['value'] in [None, '.']:
                    logging.warning(f"Pominięto nieprawidłową wartość dla daty {data_point.get('date', 'unknown')}: {data_point.get('value', 'unknown')}")
                    continue

                # Konwersja wartości na odpowiedni format
                price = float(data_point['value'])

                converted_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                existing_entry = db.session.query(CurrencyData).filter(
                CommodityData.date == converted_date,
                CommodityData.name == name
                ).first()


                # Dodanie nowego wpisu, jeśli nie istnieje
                if existing_entry is None:
                    new_commodity = CommodityData(
                        name=name,
                        date=datetime.strptime(data_point['date'], '%Y-%m-%d').date(),
                        price=price,
                        unit=commodity_data.get('unit', 'not provided')
                    )
                    db.session.add(new_commodity)
            except ValueError as e:
                logging.error(f"Błąd konwersji danych towarowych dla daty {data_point.get('date', 'unknown')}: {e}")
                continue

        # Zapisanie zmian w bazie danych
        db.session.commit()
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {e}")
        return f"Request Exception: {e}"
    except ValueError:
        logging.error("Invalid JSON response from API.")
        return "Invalid JSON response from API."
    


       
def fetch_and_save_stock_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        stock_data_json = response.json()
        logging.info(f"Odpowiedź API dla {symbol}: {stock_data_json}")  # Dodano dla lepszego logowania

        is_valid, message = validate_stock_data_structure(stock_data_json)
        if not is_valid:
            logging.error(message)
            return message

        if 'Time Series (Daily)' not in stock_data_json:
            logging.error("Expected key 'Time Series (Daily)' not found in the JSON response.")
            return "Expected key 'Time Series (Daily)' not found in the JSON response."

        for date_str, daily_data in stock_data_json['Time Series (Daily)'].items():
            if any(value is None for value in daily_data.values()):
                logging.warning(f"Pominięto niekompletne dane dla daty {date_str}")
                continue

            try:
                open_price = float(daily_data['1. open'])
                high_price = float(daily_data['2. high'])
                low_price = float(daily_data['3. low'])
                close_price = float(daily_data['4. close'])
                volume = int(daily_data['5. volume'])

                existing_entry = db.session.query(StockData).filter(
                    StockData.date == date_str,
                    StockData.symbol == symbol
                ).first()

                if existing_entry is None:
                    new_entry = StockData(
                        symbol=symbol,
                        date=date_str,
                        close_price=close_price,
                        volume=volume
                    )
                    db.session.add(new_entry)
                    
            except Exception as e:  # Ulepszona obsługa wyjątków
                logging.error(f"Błąd podczas dodawania wpisu dla {date_str}: {e}")

        # Zapisanie zmian w bazie danych
        db.session.commit()
        logging.info("Zatwierdzono transakcję w bazie danych.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {e}")
        return f"Request Exception: {e}"
    except ValueError as e:
        logging.error(f"Invalid JSON response from API: {e}")
        return "Invalid JSON response from API."
    except Exception as e:  # Dodatkowa obsługa ogólnych wyjątków
        logging.error(f"Ogólny błąd: {e}")
        db.session.rollback()



def fetch_and_save_inflation_data(api_key, db_session):
    url = f'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        inflation_data = response.json()

        if 'data' not in inflation_data:
            return "Key 'data' not found in API response."

        for data_point in inflation_data['data']:
            if 'value' not in data_point or data_point['value'] is None:
                continue
            date = datetime.strptime(data_point['date'], '%Y-%m-%d').date()
            value = float(data_point['value'])

            existing_entry = db_session.query(CPI_Data).filter(CPI_Data.date == date).first()

            if existing_entry is None:
                new_cpi_data = CPI_Data(date=date, value=value)  # Ustaw inflację jako None
                db_session.add(new_cpi_data)

        db_session.commit()
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
    elif data_type == 'rsi_data':
        return db.session.query(RsiData).filter(RsiData.date == date).count() > 0

    else:
        raise ValueError("Nieznany typ danych")

    return False
    

   
def populate_time_dimension(start_year=2000, end_year=None):

    if end_year is None:
        end_year = date.today().year

    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)

    current_date = start_date
    while current_date <= end_date:
        if not TimeDimension.query.get(current_date):
            time_record = TimeDimension(current_date)
            db.session.add(time_record)
        current_date += timedelta(days=1)

    db.session.commit()

# Tworzenie silnika bazy danych (upewnij się, że używasz swojego URL bazy danych)
engine = create_engine('mssql+pyodbc://aa')
Session = sessionmaker(bind=engine)
session = Session()



def fetch_ema_data(symbol, interval, time_period, series_type,api_key):
    url = f'https://www.alphavantage.co/query?function=EMA&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ema_data = data['Technical Analysis: EMA']
        df = pd.DataFrame.from_dict(ema_data).T
        df.index.name = 'date'
        df.reset_index(inplace=True)
        df['symbol'] = symbol
        return df
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()

def save_ema_data_to_db(df,time_period):
    session = Session()
    for index, row in df.iterrows():
        ema_record = EmaData(
            symbol=row['symbol'],
            date=row['date'],
            ema=row['EMA'],
            time_period=time_period
        )
        session.add(ema_record)
    session.commit()
    session.close()

def fetch_rsi_data(symbol, interval, time_period, series_type, api_key):
    url = f"https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        rsi_data = response.json()['Technical Analysis: RSI']
        df = pd.DataFrame.from_dict(rsi_data, orient='index')
        
        # Używam 'coerce' w przypadku błędów, co spowoduje ustawienie NaT (Not a Time) dla problematycznych dat
        df.index = pd.to_datetime(df.index, errors='coerce')
        
        # Odfiltruj wiersze, w których index (data) nie został poprawnie przekształcony
        df = df[df.index.notnull()]

        df['symbol'] = symbol
        df['time_period'] = time_period
        df.rename(columns={'RSI': 'rsi'}, inplace=True)
        return df
    else:
        print(f"Error fetching RSI data: {response.status_code}")
        return pd.DataFrame()
def save_rsi_data_to_db(df):
    session = Session()
    for index, row in df.iterrows():
        rsi_record = RsiData(
            symbol=row['symbol'],
            date=index.date(),
            rsi=row['rsi'],
            time_period=row['time_period']
        )
        session.add(rsi_record)
    session.commit()
    session.close()   


def calculate_and_save_correlations():
    session = Session()
    
    # Pobieranie danych
    cpi_df = pd.read_sql(session.query(CPI_Data).statement, session.bind)
    interest_rate_df = pd.read_sql(session.query(InterestRateData).statement, session.bind)
    currency_df = pd.read_sql(session.query(CurrencyData).statement, session.bind)
    commodity_df = pd.read_sql(session.query(CommodityData).statement, session.bind)
    stock_df = pd.read_sql(session.query(StockData).statement, session.bind)

    # Przygotowanie danych
    cpi_df['date'] = pd.to_datetime(cpi_df['date'])
    interest_rate_df['date'] = pd.to_datetime(interest_rate_df['date'])
    currency_df['date'] = pd.to_datetime(currency_df['date'])
    commodity_df['date'] = pd.to_datetime(commodity_df['date'])
    stock_df['date'] = pd.to_datetime(stock_df['date'])

    for df, asset_type, asset_column, price_column in [
        (currency_df, 'Currency', 'symbol', 'close_price'), 
        (commodity_df, 'Commodity', 'name', 'price'), 
        (stock_df, 'Stock', 'symbol', 'close_price')
    ]:
        if asset_column in df.columns:
            for asset_symbol in df[asset_column].unique():
                asset_df = df[df[asset_column] == asset_symbol]

                # Usunięcie kolumn nieliczbowych i dodanie daty
                asset_df_numeric = asset_df.select_dtypes(include=[np.number])
                asset_df_numeric['date'] = asset_df['date']

                # Łączenie z CPI i stopami procentowymi
                merged_df_cpi = asset_df_numeric.merge(cpi_df[['date', 'value']], on='date', how='inner')
                merged_df_interest = asset_df_numeric.merge(interest_rate_df[['date', 'value']], on='date', how='inner')

                # Sprawdzenie czy DataFrame jest pusty i oblicz korelację
                if not merged_df_cpi.empty and price_column in merged_df_cpi.columns:
                    cpi_corr = merged_df_cpi[[price_column, 'value']].corr().iloc[0, 1]

                if not merged_df_interest.empty and price_column in merged_df_interest.columns:
                    interest_rate_corr = merged_df_interest[[price_column, 'value']].corr().iloc[0, 1]

                # Zapisz wynik do bazy danych
                correlation_data = CorrelationData(
                    asset_type=asset_type,
                    asset_symbol=asset_symbol,
                    correlation_with_cpi=cpi_corr,
                    correlation_with_interest_rate=interest_rate_corr,
                    date=pd.to_datetime('today').date()
                )
                session.add(correlation_data)
        else:
            print(f"DataFrame dla {asset_type} nie zawiera kolumny '{asset_column}'")

    session.commit()
    session.close()
