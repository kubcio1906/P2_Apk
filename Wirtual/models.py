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
    average_price = db.Column(db.Float, nullable=False)
    
   
    def __init__(self, symbol, date, open_price, high_price, low_price, close_price, average_price):
        self.symbol = symbol
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.average_price = average_price
    def __repr__(self):
        return f"<CurrencyData {self.symbol} {self.date} Open: {self.open_price} High: {self.high_price} Low: {self.low_price} Close: {self.close_price} Average: {self.average_price}>"
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
    average_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)  # Wolumen może być dużą liczbą, więc używamy BigInteger
   

    def __init__(self, symbol, date, average_price, volume):
        self.symbol = symbol
        self.date = datetime.strptime(date, '%Y-%m-%d').date()
        self.average_price = average_price
        self.volume = volume
    def __repr__(self):
        return f"<StockData {self.symbol} {self.date} Average Price: {self.average_price} Volume: {self.volume}>"

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
    __tablename__ = 'retail_sales_data'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __init__(self, date, value):
        self.date = date
        self.value = value

    def __repr__(self):
        return f"<RetailSalesData {self.date} Value: {self.value}>"


