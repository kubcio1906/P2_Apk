from views import fetch_and_save_commodity_data, fetch_and_save_fx_data, fetch_and_save_inflation_data, fetch_and_save_interest_rates_data, fetch_and_save_stock_data, data_exists_in_database
from models import CurrencyData, CommodityData, StockData, CPI_Data, InterestRateData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import requests
import pandas as pd
import seaborn as sns
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





def calculate_ema(data, days):
    """
    Oblicza EMA dla podanej liczby dni.
    :param data: Lista z danymi cenowymi.
    :param days: Liczba dni do obliczenia EMA (np. 50 lub 200).
    :return: Lista z wartościami EMA.
    """
    ema_values = [None] * (days - 1)  # Wypełnienie dla dni bez danych EMA
    k = 2 / (days + 1)
    
    # Początkowa wartość EMA to średnia z pierwszych 'days' dni
    ema_yesterday = sum(data[:days]) / days
    ema_values.append(ema_yesterday)

    # Obliczanie EMA dla każdego kolejnego dnia
    for price in data[days:]:
        ema_today = (price * k) + (ema_yesterday * (1 - k))
        ema_values.append(ema_today)
        ema_yesterday = ema_today
    return ema_values

engine = create_engine('mssql+pyodbc://aa')
Session = sessionmaker(bind=engine)


def get_data_from_db(model, start_date, end_date):
    session = Session()
    try:
        query = session.query(model.date, model.value).filter(model.date >= start_date, model.date <= end_date)
        data = pd.read_sql(query.statement, session.bind)
    finally:
        session.close()
    return data.set_index('date').sort_index()

cpi_data = get_data_from_db(CPI_Data, '2020-01-01', '2021-01-01')
interest_rate_data = get_data_from_db(InterestRateData, '2020-01-01', '2021-01-01')
print(len)

def plot_correlation(data1, data2, title):
    combined_data = pd.concat([data1, data2], axis=1).dropna()
    correlation = combined_data.corr().iloc[0, 1]

    plt.figure(figsize=(10, 6))
    # Używamy nazw kolumn bezpośrednio zamiast odwoływać się do nich przez combined_data.columns
    sns.scatterplot(x=combined_data.iloc[:, 0], y=combined_data.iloc[:, 1], data=combined_data)
    plt.title(f"{title}\nKorelacja: {correlation:.2f}")
    plt.xlabel(combined_data.columns[0])
    plt.ylabel(combined_data.columns[1])
    plt.show()

plot_correlation(cpi_data, interest_rate_data, 'Korelacja między CPI a stopami procentowymi')

# Obliczanie EMA dla danych cenowych akcji
#stock_ema_50 = calculate_ema(stock_prices, 50)

session = Session()
symbol = 'USDPLN'
liczba_dni = 865
query = session.query(CurrencyData.close_price, CurrencyData.date).filter(CurrencyData.symbol == symbol).order_by(CurrencyData.date.desc()).limit(liczba_dni)
forex_prices = [record.close_price for record in query.all()]
forex_dates = [record.date for record in query.all()]
session.close()

forex_dates = []
for record in query.all():
    forex_dates.append(record.date)

forex_ema_20 = calculate_ema(forex_prices,20)
forex_ema_50 = calculate_ema(forex_prices, 50)
forex_ema_200 = calculate_ema(forex_prices, 200)




def plot_ema(dates, prices,ema_20, ema_50, ema_200, title):
    plt.figure(figsize=(30, 15))
    plt.plot(dates, prices, label='Ceny', color='blue')
    plt.plot(dates, ema_20, label='EMA 20', color='black')
    plt.plot(dates, ema_50, label='EMA 50', color='red')
    plt.plot(dates, ema_200, label='EMA 200', color='green')
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Cena')
    plt.xticks(rotation=45)  # Obraca etykiety dat
    plt.legend()
    plt.show()

plot_ema(forex_dates,forex_prices,forex_ema_20,forex_ema_50, forex_ema_200, 'Wykres EMA dla EURPLN')


