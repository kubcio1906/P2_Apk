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
    related_news = db.relationship('NewsArticle', secondary='currency_news_link')
    def __init__(self, symbol, date, open_price, high_price, low_price, close_price, average_price):
        self.symbol = symbol
        self.date = date
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.average_price = average_price

class CommodityData(db.Model):
    __tablename__ = 'commodity_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=True)
    related_news = db.relationship('NewsArticle', secondary='commodity_news_link')

    def __init__(self, name, date, price, unit):
        self.name = name
        self.date = date
        self.price = price
        self.unit = unit

class StockData(db.Model):
    __tablename__ = 'stock_data'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    average_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.BigInteger, nullable=False)  # Wolumen może być dużą liczbą, więc używamy BigInteger
    related_news = db.relationship('NewsArticle', secondary='stock_news_link')

    def __init__(self, symbol, date, average_price, volume):
        self.symbol = symbol
        self.date = datetime.strptime(date, '%Y-%m-%d').date()
        self.average_price = average_price
        self.volume = volume



class NewsArticle(db.Model):
    __tablename__ = 'news_article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    publication_date = db.Column(db.Date)
    summary = db.Column(db.Text, nullable=False)
    banner_image = db.Column(db.String(500), nullable=True)
    source_id = db.Column(db.Integer, db.ForeignKey('news_source.id'), nullable=False)
    overall_sentiment_score = db.Column(db.Float, nullable=False)
    overall_sentiment_label = db.Column(db.String(50), nullable=False)

    # Relationship to NewsSource
    source = db.relationship('NewsSource', back_populates='articles')
    related_currencies = db.relationship('CurrencyData', secondary='currency_news_link')
    related_commodities = db.relationship('CommodityData', secondary='commodity_news_link')
    related_stocks = db.relationship('StockData', secondary='stock_news_link')

class NewsSource(db.Model):
    __tablename__ = 'news_source'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)
    category_within_source = db.Column(db.String(100), nullable=True)
    source_domain = db.Column(db.String(100), nullable=False)
    
    # Relationship to NewsArticle
    articles = db.relationship('NewsArticle', back_populates='source')

class NewsTopic(db.Model):
    __tablename__ = 'news_topic'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    relevance_score = db.Column(db.Float, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('news_article.id'), nullable=False)

    # Relationship to NewsArticle
    article = db.relationship('NewsArticle', backref=db.backref('topics', lazy=True))

class TickerSentiment(db.Model):
    __tablename__ = 'ticker_sentiment'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    relevance_score = db.Column(db.Float, nullable=False)
    ticker_sentiment_score = db.Column(db.Float, nullable=False)
    ticker_sentiment_label = db.Column(db.String(50), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('news_article.id'), nullable=False)

    # Relationship to NewsArticle
    article = db.relationship('NewsArticle', backref=db.backref('ticker_sentiments', lazy=True))

stock_news_link = db.Table('stock_news_link',
    db.Column('stock_id', db.Integer, db.ForeignKey('stock_data.id'), primary_key=True),
    db.Column('news_article_id', db.Integer, db.ForeignKey('news_article.id'), primary_key=True)
)
currency_news_link = db.Table('currency_news_link',
    db.Column('currency_data_id', db.Integer, db.ForeignKey('currency_data.id'), primary_key=True),
    db.Column('news_article_id', db.Integer, db.ForeignKey('news_article.id'), primary_key=True)
)
commodity_news_link = db.Table('commodity_news_link',
    db.Column('commodity_data_id', db.Integer, db.ForeignKey('commodity_data.id'), primary_key=True),
    db.Column('news_article_id', db.Integer, db.ForeignKey('news_article.id'), primary_key=True)
)