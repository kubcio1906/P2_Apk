from flask import  jsonify,current_app
from extensions import db
from models import CurrencyData, CommodityData, StockData, NewsSource, NewsArticle, NewsTopic, TickerSentiment, InflationData, commodity_news_link, currency_news_link, stock_news_link
from datetime import datetime
import requests
from sqlalchemy.exc import SQLAlchemyError




def fetch_and_save_fx_data(symbol,api_key):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&outputsize=full&apikey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        fx_data = response.json()
        if 'Time Series FX (Daily)' not in fx_data:
            return f"Key 'Time Series FX (Daily)' not found in API response for symbol {symbol}."

        for date_str, daily_data in fx_data['Time Series FX (Daily)'].items():
            print(f"Data for {date_str}: {daily_data}")  # Dodaj tę linię
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
    response = requests.get(url)
    if response.status_code == 200:
        inflation_data = response.json()
        if 'data' in inflation_data:
            for data_point in inflation_data['data']:
                date = datetime.strptime(data_point['date'], '%Y-%m-%d').date()
                value = float(data_point['value'])

                # Sprawdzanie, czy dane za ten miesiąc już istnieją
                existing_entry = InflationData.query.filter_by(date=date).first()
                if not existing_entry:
                    new_entry = InflationData(date=date, value=value)
                    db.session.add(new_entry)
            db.session.commit()
            return "Inflation data fetched and saved successfully."
        else:
            return "Expected key 'data' not found in the JSON response."
    else:
        return "Failed to fetch data from API."

def fetch_and_save_news_data(api_key, tickers=None, topics=None, time_from=None, time_to=None, sort='LATEST', limit=1000):
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "apikey": api_key,
        "tickers": tickers,
        "topics": topics,
        "time_from": time_from,
        "time_to": time_to,
        "sort": sort,
        "limit": limit
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        news_data = response.json()
        print(news_data)
        if 'feed' in news_data:
            for item in news_data['feed']:
                # Konwersja czasu publikacji na obiekt datetime
                time_published = datetime.strptime(item['time_published'], '%Y%m%dT%H%M%S')

                # Utwórz i dodaj artykuł wiadomości
                article = NewsArticle(
                    title=item['title'],
                    url=item['url'],
                    publication_date=time_published,
                    summary=item['summary'],
                    banner_image=item.get('banner_image'),
                    overall_sentiment_score=item.get('overall_sentiment_score', 0.0),
                    overall_sentiment_label=item.get('overall_sentiment_label', 'Neutral')
                )
                db.session.add(article)
                db.session.flush()  # To pozwala na odzyskanie ID dla obiektu przed zapisem

                # Dodaj informacje o tematach
                for topic in item.get('topics', []):
                    new_topic = NewsTopic(
                        topic=topic['topic'],
                        relevance_score=float(topic['relevance_score']),
                        article_id=article.id
                    )
                    db.session.add(new_topic)

                # Dodaj informacje o sentymentach tickerów
                for ticker_sentiment in item.get('ticker_sentiment', []):
                    new_ticker_sentiment = TickerSentiment(
                        ticker=ticker_sentiment['ticker'],
                        relevance_score=float(ticker_sentiment['relevance_score']),
                        ticker_sentiment_score=float(ticker_sentiment['ticker_sentiment_score']),
                        ticker_sentiment_label=ticker_sentiment['ticker_sentiment_label'],
                        article_id=article.id
                    )
                    db.session.add(new_ticker_sentiment)
                
            db.session.commit()
            process_news_data(news_data)
            return "News data fetched and saved successfully."
        else:
            return "Expected key 'feed' not found in the JSON response."
    else:
        return "Failed to fetch data from API."
def process_news_data(json_data):
    max_ticker_length = 20  # Zakładając, że maksymalna długość to 10 znaków
    # Zakładam, że już masz sesję bazy danych
    for entry in json_data['feed']:
        # Utwórz i dodaj artykuł wiadomości
        article = NewsArticle(
            title=entry['title'],
            url=entry['url'],
            publication_date=datetime.strptime(entry['time_published'], '%Y%m%dT%H%M%S'),
            summary=entry['summary'],
            banner_image=entry['banner_image'],
            overall_sentiment_score=entry['overall_sentiment_score'],
            overall_sentiment_label=entry['overall_sentiment_label']
        )
        db.session.add(article)
        db.session.flush()  # Pobierz ID dla artykułu przed zapisaniem

        # Utwórz i dodaj źródło, jeśli jeszcze nie istnieje
        source = NewsSource.query.filter_by(source_domain=entry['source_domain']).first()
        if not source:
            source = NewsSource(
                source=entry['source'],
                category_within_source=entry['category_within_source'],
                source_domain=entry['source_domain']
            )
            db.session.add(source)
            db.session.flush()  # Pobierz ID dla źródła przed zapisaniem
        
        # Przypisz źródło do artykułu
        article.source_id = source.id

        # Dodaj tematy
        for topic in entry['topics']:
            new_topic = NewsTopic(
                topic=topic['topic'],
                relevance_score=topic['relevance_score'],
                article_id=article.id
            )
            db.session.add(new_topic)

        # Dodaj sentymenty tickerów
        for ticker_sentiment in entry['ticker_sentiment']:
            new_ticker_sentiment = TickerSentiment(
                ticker=ticker_sentiment['ticker'],
                relevance_score=ticker_sentiment['relevance_score'],
                ticker_sentiment_score=ticker_sentiment['ticker_sentiment_score'],
                ticker_sentiment_label=ticker_sentiment['ticker_sentiment_label'],
                article_id=article.id
            )
            db.session.add(new_ticker_sentiment)

        for ticker_sentiment in entry['ticker_sentiment']:
            ticker = ticker_sentiment['ticker'][:max_ticker_length]  # Obcinanie tickeru do maksymalnej długości

            new_ticker_sentiment = TickerSentiment(
                ticker=ticker,
                relevance_score=float(ticker_sentiment['relevance_score']),
                ticker_sentiment_score=float(ticker_sentiment['ticker_sentiment_score']),
                ticker_sentiment_label=ticker_sentiment['ticker_sentiment_label'],
                article_id=article.id
            )
            db.session.add(new_ticker_sentiment)
        for currency in find_related_currencies(entry):
            association = currency_news_link.insert().values(
                currency_data_id=currency.id,
                news_article_id=article.id
            )
            db.session.execute(association)

        # Przypisanie artykułu do towarów
        for commodity in find_related_commodities(entry):
            association = commodity_news_link.insert().values(
                commodity_data_id=commodity.id,
                news_article_id=article.id
            )
            db.session.execute(association)

        # Przypisanie artykułu do akcji
        for stock in find_related_stocks(entry):
            association = stock_news_link.insert().values(
                stock_id=stock.id,
                news_article_id=article.id
            )
            db.session.execute(association)

    db.session.commit()

def find_related_currencies(news_item):
    related_currencies = []
    title = news_item['title']
    currency_symbols = ["USD", "EUR", "PLN"]
    for symbol in currency_symbols:
        if symbol in title:
            try:
                currency = CurrencyData.query.filter_by(symbol=symbol).first()
                if currency:
                    related_currencies.append(currency)
            except SQLAlchemyError as e:
                current_app.logger.error(f"Błąd bazy danych przy próbie wyszukania waluty: {e}")
    return related_currencies
    
def find_related_commodities(news_item):
    related_commodities = []
    title = news_item['title']
    # Lista towarów, które mogą być wspomniane w artykule
    commodity_names = ["BRENT", "NATURAL_GAS", "COPPER", "ALUMINUM", "COFFEE"]
    for name in commodity_names:
        if name in title:
            try:
                commodity = CommodityData.query.filter_by(name=name).first()
                if commodity:
                    related_commodities.append(commodity)
            except SQLAlchemyError as e:
                current_app.logger.error(f"Błąd bazy danych przy próbie wyszukania commodity: {e}")
    return related_commodities

def find_related_stocks(news_item):
    related_stocks = []
    title = news_item['title']

    # Zakładamy, że mamy listę tickerów giełdowych
    stock_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "FB", "TSLA", "BRK.A", "V", "JNJ", "WMT","NVDA"]

    for symbol in stock_symbols:
        if symbol in title:
            try:
                stock = StockData.query.filter_by(symbol=symbol).first()
                if stock:
                    related_stocks.append(stock)
            except SQLAlchemyError as e:
                current_app.logger.error(f"Błąd bazy danych przy próbie wyszukania stock: {e}")

    return related_stocks



def setup_routes(app):

  #  @app.route('/fetch_fx_data/<string:symbol>', methods=['GET'])
   # def fetch_fx_data_view(symbol):
    #    result = fetch_and_save_fx_data(symbol)
    #   if result == "Data fetched and saved successfully.":
    #        response = {"status": "success", "message": result}
    #    else:
    #        response = {"status": "error", "message": result}
    #    return jsonify(response)
    
    # Endpoint do pobierania danych o towarach
    
    @app.route('/fetch_commodity_data/<string:name>', methods=['GET'])
    def fetch_commodity_data_view(name):
        result = fetch_and_save_commodity_data(name)
        if result == "Commodity data fetched and saved successfully.":
            return jsonify({'status': 'success', 'message': result}), 200
        else:
            return jsonify({'status': 'error', 'message': result}), 500

    @app.route('/fetch_stock_data/<string:symbol>', methods=['GET'])
    def fetch_stock_data(symbol):
      
        result = fetch_and_save_stock_data(symbol)
        if result == "Stock data fetched and saved successfully.":
           response = {"status": "success", "message": result}
        else:
            response = {"status": "error", "message": result}
        return jsonify(response)
    
    @app.route('/fetch_news_data/<string:ticker>', methods=['GET'])
    def fetch_news_data(ticker):
      
        result = fetch_and_save_news_data(ticker)
        if result == "News data fetched and saved successfully.":
            return jsonify({'status': 'success', 'message': result}), 200
        else:
            return jsonify({'status': 'error', 'message': result}), 500
def auto_fetch_currency_pairs(api_key):
   
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

def auto_fetch_news_data(api_key):
    fetch_and_save_news_data(api_key)