from sqlalchemy import func
from views import( fetch_and_save_commodity_data, fetch_and_save_fx_data, fetch_and_save_inflation_data, fetch_and_save_interest_rates_data,
                   fetch_and_save_stock_data,fetch_ema_data,save_ema_data_to_db,fetch_rsi_data,save_rsi_data_to_db
                  )
from models import CurrencyData, CommodityData, StockData, CPI_Data, InterestRateData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, update, extract
import requests
import logging
import pandas as pd
def auto_fetch_currency_data(api_key):
   
    base_currencies = ["EUR","USD","CHF","JPY"] #, "EUR", "CHF", "GBP"
    target_currencies = ["PLN"] #, "EUR", "CHF", "GBP"

    for base_currency in base_currencies:
        for target_currency in target_currencies:
            if base_currency != target_currency:
                symbol = base_currency + target_currency
                fetch_and_save_fx_data(symbol, api_key)
def auto_fetch_commodity_data(api_key):
    
    commodities = ["BRENT", "NATURAL_GAS","COPPER", "COFFEE"]

    for commodity in commodities:
        fetch_and_save_commodity_data(commodity,api_key)
def auto_fetch_stock_data(api_key):
 
    # Lista symboli  najpopularniejszych spółek
    stock_symbols = ['MSFT','IBM']

    for symbol in stock_symbols:
        fetch_and_save_stock_data(symbol,api_key)



def auto_fetch_inflation_data(api_key,db_session):
    
    fetch_and_save_inflation_data(api_key,db_session)

def auto_fetch_save_interest_rates_data(api_key):
    
    fetch_and_save_interest_rates_data(api_key)


def calculate_inflation_from_cpi(db_session):
    # Pobierz wszystkie rekordy CPI, posortowane od najstarszego do najnowszego
    cpi_records = db_session.query(CPI_Data).order_by(CPI_Data.date).all()

   
    for i in range(1, len(cpi_records)):
        current_record = cpi_records[i]
        previous_record = cpi_records[i - 1]

        # Upewnij się, że oba wpisy są z kolejnych miesięcy
        if (current_record.date.year == previous_record.date.year and
            current_record.date.month == previous_record.date.month + 1) or \
           (current_record.date.year == previous_record.date.year + 1 and
            current_record.date.month == 1 and previous_record.date.month == 12):

            # Oblicz inflację i zaktualizuj bieżący rekord
            try:
                inflation_rate = ((current_record.value - previous_record.value) / previous_record.value) * 100
                current_record.inflation_rate = inflation_rate
            except ZeroDivisionError as e:
                logging.error(f"Division by zero error for CPI record with id {previous_record.id}: {e}")
                continue

   
    db_session.commit()

def auto_fetch_ema_data(api_key, symbols, intervals, time_periods, series_types):
    for symbol in symbols:
        for interval in intervals:
            for time_period in time_periods:
                for series_type in series_types:
                    df_ema = fetch_ema_data(symbol, interval, time_period, series_type, api_key)
                    if not df_ema.empty:
                        save_ema_data_to_db(df_ema,time_period)

def auto_fetch_rsi_data(api_key, symbols, intervals, time_periods, series_types):
    for symbol in symbols:
        for interval in intervals:
            for time_period in time_periods:
                for series_type in series_types:
                    df_rsi = fetch_rsi_data(symbol, interval, time_period, series_type, api_key)
                    if not df_rsi.empty:
                        save_rsi_data_to_db(df_rsi)

