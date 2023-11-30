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
    stock_symbols = ["AAPL"]#, "MSFT", "AMZN", "GOOGL", "FB", "TSLA", "BRK.A", "V", "JNJ", "WMT","NVDA"]

    for symbol in stock_symbols:
        fetch_and_save_stock_data(symbol,api_key)

def auto_fetch_inflation_data(api_key):
    
    fetch_and_save_inflation_data(api_key)

def auto_fetch_save_interest_rates_data(api_key):
    
    fetch_and_save_interest_rates_data(api_key)


def calculate_yearly_inflation(cpi_data, year):
    """
    Oblicza zmianę procentową inflacji każdego miesiąca od początku wybranego roku.

    :param cpi_data: DataFrame z Pandas zawierający dane CPI, gdzie indeks to daty, a kolumna zawiera wartości CPI.
    :param year: Rok, dla którego ma być obliczona inflacja.
    :return: DataFrame z obliczoną miesięczną inflacją względem początku roku.
    """
    # Upewnij się, że indeks jest typu datetime
    cpi_data.index = pd.to_datetime(cpi_data.index)

    # Filtruj dane dla wybranego roku
    yearly_data = cpi_data[cpi_data.index.year >= year]

    # Oblicz inflację względem początku roku
    start_of_year_value = yearly_data.loc[str(year)].iloc[0]
    inflation_from_start_of_year = (yearly_data - start_of_year_value) / start_of_year_value * 100

    # Zmień nazwę kolumny na 'Inflation from Start of Year'
    inflation_from_start_of_year.columns = ['Inflation from Start of Year']

    return inflation_from_start_of_year




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

def get_commodity_data_from_db(commodity_name, start_date, end_date):
    session = Session()
    try:
        query = session.query(CommodityData.date, CommodityData.price).filter(
            CommodityData.name == commodity_name,
            CommodityData.date >= start_date, 
            CommodityData.date <= end_date
        )
        data = pd.read_sql(query.statement, session.bind)
    finally:
        session.close()
    return data.set_index('date').sort_index()

def get_stock_data_from_db(stock_symbol, start_date, end_date):
    session = Session()
    try:
        query = session.query(StockData.date, StockData.average_price).filter(
            StockData.symbol == stock_symbol,
            StockData.date >= start_date, 
            StockData.date <= end_date
        )
        data = pd.read_sql(query.statement, session.bind)
    finally:
        session.close()
    return data.set_index('date').sort_index()

def get_data_from_db(model, start_date, end_date):
    session = Session()
    try:
        query = session.query(model.date, model.value).filter(model.date >= start_date, model.date <= end_date)
        data = pd.read_sql(query.statement, session.bind)
    finally:
        session.close()
    return data.set_index('date').sort_index()

"""cpi_data = get_data_from_db(CPI_Data, '2015-01-01', '2023-01-01')
inflation_data = calculate_yearly_inflation(cpi_data,2015)
interest_rate_data = get_data_from_db(InterestRateData, '2015-01-01', '2023-01-01')
print(len)

def analyze_inflation_forex_pair_relation(inflation_data, forex_pair_data, forex_pair_name, title):
    # Połączenie danych inflacji i konkretnej pary walutowej
    combined_data = pd.concat([inflation_data, forex_pair_data], axis=1).dropna()

    # Obliczenie korelacji
    correlation = combined_data.corr().iloc[0, 1]

    # Tworzenie wykresu
    plt.figure(figsize=(12, 6))

    # Wykres liniowy dla inflacji
    ax1 = plt.gca()
    ax1.plot(combined_data.index, combined_data.iloc[:, 0], color='blue', label='Inflacja')
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Inflacja', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Wykres liniowy dla pary walutowej na drugiej osi Y
    ax2 = ax1.twinx()
    ax2.plot(combined_data.index, combined_data.iloc[:, 1], color='green', label=forex_pair_name)
    ax2.set_ylabel('Cena Forex', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    # Tytuł i legenda
    plt.title(f"{title}\nKorelacja: {correlation:.2f}")
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.show()"""

# Przygotowanie danych Forex
session = Session()
symbol = 'USDPLN'
liczba_dni = 2000
query = session.query(CurrencyData.close_price, CurrencyData.date).filter(CurrencyData.symbol == symbol).order_by(CurrencyData.date.desc()).limit(liczba_dni)
forex_prices = [record.close_price for record in query.all()]
forex_dates = [record.date for record in query.all()]
session.close()

# Tworzenie DataFrame z danych Forex
forex_data = pd.DataFrame({'Forex_Price': forex_prices}, index=forex_dates)

# Wywołanie funkcji analyze_inflation_forex_pair_relation
#analyze_inflation_forex_pair_relation(inflation_data, forex_data['Forex_Price'], 'USDPLN', 'Relacja między inflacją a ceną USDPLN')

forex_dates = []
for record in query.all():
    forex_dates.append(record.date)

forex_ema_20 = calculate_ema(forex_prices,20)
forex_ema_50 = calculate_ema(forex_prices, 50)
forex_ema_200 = calculate_ema(forex_prices, 200)

"""def plot_interest_rates(interest_rate_data, title):
    plt.figure(figsize=(12, 6))
    plt.plot(interest_rate_data.index, interest_rate_data['value'], label='Stopa Procentowa', color='purple')
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Stopa Procentowa')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

# Przykładowe wywołanie
plot_interest_rates(interest_rate_data, 'Wykres Stóp Procentowych')"""

"""def plot_commodity_data(commodity_data, commodity_name, title):
    plt.figure(figsize=(12, 6))
    plt.plot(commodity_data.index, commodity_data['price'], label=commodity_name, color='orange')
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Cena Towaru')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

# Przykładowe wywołanie
# Załóżmy, że mamy dane o cenie ropy Brent
brent_data = get_commodity_data_from_db('BRENT', '2015-01-01', '2023-01-01')
plot_commodity_data(brent_data, 'BRENT', 'Wykres Ceny Ropy Brent')"""

def plot_stock_data(stock_data, stock_symbol, title):
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index, stock_data['average_price'], label=stock_symbol, color='green')
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Cena Akcji')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

# Przykładowe wywołanie
# Załóżmy, że mamy dane o akcjach Apple
stock_data = get_stock_data_from_db('AAPL', '2023-07-11', '2023-11-29')
print(stock_data)
plot_stock_data(stock_data, 'AAPL', 'Wykres Ceny Akcji Apple')


"""def plot_ema(dates, prices,ema_20, ema_50, ema_200, title):
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

plot_ema(forex_dates,forex_prices,forex_ema_20,forex_ema_50, forex_ema_200, 'Wykres EMA dla EURPLN')"""


