from extensions import db
from datetime import datetime
# Instancja SQLAlchemy powinna być stworzona w głównym pliku aplikacji i importowana tutaj
# from yourapp import db



# Model danych reprezentujący dane FX Daily
class CurrencyData(db.Model):
    __tablename__ = 'currency_data'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
   
    
   
    def __init__(self, symbol, date, open_price, high_price, low_price, close_price):
        self.symbol = symbol
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
       
    def __repr__(self):
        return f"<CurrencyData {self.symbol} {self.date} Open: {self.open_price} High: {self.high_price} Low: {self.low_price} Close: {self.close_price}>"
class CommodityData(db.Model):
    __tablename__ = 'commodity_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=True)
   
    
    def __init__(self, name, date, price, unit):
        self.name = name
        self.date = date
        self.price = price
        self.unit = unit
    def __repr__(self):
        return f"<CommodityData {self.name} {self.date} Price: {self.price} Unit: {self.unit}>"

class StockData(db.Model):
    __tablename__ = 'stock_data'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)  # Wolumen może być dużą liczbą, więc używamy BigInteger

   

    def __init__(self, symbol, date, close_price, volume):
        self.symbol = symbol
        self.date = datetime.strptime(date, '%Y-%m-%d').date()
        self.close_price = close_price
        self.volume = volume
    def __repr__(self):
        return f"<StockData {self.symbol} {self.date} Price: {self.close_price} Volume: {self.volume}>"

class CPI_Data(db.Model):
    __tablename__ = 'cpi_data'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    def __init__(self, date, value):
        self.date = date
        self.value = value
    def __repr__(self):
        return f"<CPI_Data {self.date} Value: {self.value}>"

class InterestRateData(db.Model):
    __tablename__ = 'interesr_rate_data'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, date, value):
        self.date = date
        self.value = value

    def __repr__(self):
        return f"<InterestRateData {self.date} Value: {self.value}>"



class TimeDimension(db.Model):
    __tablename__ = 'time_dimension'
    date = db.Column(db.Date, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)

    def __init__(self, date):
        self.date = date
        self.year = date.year
        self.quarter = (date.month - 1) // 3 + 1
        self.month = date.month
        self.day = date.day
        self.week_of_year = date.isocalendar()[1]
        self.day_of_week = date.isoweekday()

    def __repr__(self):
        return f"<TimeDimension {self.date} Y{self.year} Q{self.quarter} M{self.month} D{self.day} W{self.week_of_year} DW{self.day_of_week}>"
    
class EmaData(db.Model):
    __tablename__ = 'ema_data'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    ema = db.Column(db.Float, nullable=False)
    time_period = db.Column(db.Integer, nullable=False)  # Dodane pole określające okres EMA
    
    def __init__(self, symbol, date, ema, time_period):  # Dodaj time_period jako parametr
        self.symbol = symbol
        self.date = date
        self.ema = ema
        self.time_period = time_period  # Inicjalizacja wartości time_period
        
    def __repr__(self):
        # Zaktualizuj reprezentację stringową, aby uwzględnić time_period
        return f"<EmaData symbol={self.symbol} date={self.date} EMA={self.ema} time_period={self.time_period}>"

class RsiData(db.Model):
    __tablename__ = 'rsi_data'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    rsi = db.Column(db.Float, nullable=False)
    time_period = db.Column(db.Integer, nullable=False)
    
    def __init__(self, symbol, date, rsi, time_period):
        self.symbol = symbol
        self.date = date
        self.rsi = rsi
        self.time_period = time_period
        
    def __repr__(self):
        return f"<RsiData symbol={self.symbol} date={self.date} RSI={self.rsi} time_period={self.time_period}>"


class CorrelationData(db.Model):
    __tablename__ = 'correlation_data'

    id = db.Column(db.Integer, primary_key=True)
    asset_type = db.Column(db.String(50), nullable=False)  # np. 'Currency', 'Commodity', 'Stock'
    asset_symbol = db.Column(db.String(50), nullable=False)  # Symbol aktywa, np. 'EURPLN', 'BRENT', 'AAPL'
    correlation_with_cpi = db.Column(db.Float, nullable=True)  # Korelacja z CPI
    correlation_with_interest_rate = db.Column(db.Float, nullable=True)  # Korelacja ze stopami procentowymi
    date = db.Column(db.Date, nullable=False)  # Data, dla której obliczono korelację

    def __init__(self, asset_type, asset_symbol, correlation_with_cpi, correlation_with_interest_rate, date):
        self.asset_type = asset_type
        self.asset_symbol = asset_symbol
        self.correlation_with_cpi = correlation_with_cpi
        self.correlation_with_interest_rate = correlation_with_interest_rate
        self.date = date

    def __repr__(self):
        return f"<CorrelationData {self.asset_type} {self.asset_symbol} CPI_Corr: {self.correlation_with_cpi} IR_Corr: {self.correlation_with_interest_rate} Date: {self.date}>"