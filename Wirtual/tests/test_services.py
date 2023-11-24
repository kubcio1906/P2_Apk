
import unittest
from unittest.mock import patch
from app.services import fetch_and_save_fx_data
from app.views import fetch_and_save_fx_data
import requests
class TestCurrencyData(unittest.TestCase):

    @patch('app.data_fetchers.requests.get')
    def test_fetch_and_save_fx_data_success(self, mock_get):
        # Przygotowanie danych testowych
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Meta Data": {
                "1. Information": "Forex Daily Prices (open, high, low, close)",
                "2. From Symbol": "EUR",
                "3. To Symbol": "USD",
                "4. Output Size": "Compact",
                "5. Last Refreshed": "2023-11-24 13:35:00",
                "6. Time Zone": "UTC"
            },
            "Time Series FX (Daily)": {
                "2023-11-24": {
                    "1. open": "1.09040",
                    "2. high": "1.09282",
                    "3. low": "1.08947",
                    "4. close": "1.09079"
                },
                # ... (inne dane)
            }
        }

        # Wywołanie funkcji
        result = fetch_and_save_fx_data('EURUSD', 'your_api_key')

        # Sprawdzenie wyniku
        self.assertIsNone(result)  # Zakładając, że funkcja zwraca None w przypadku sukcesu

    @patch('app.data_fetchers.requests.get')
    def test_fetch_and_save_fx_data_failure(self, mock_get):
        # Symulacja błędu sieciowego
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Wywołanie funkcji
        result = fetch_and_save_fx_data('EURUSD', 'your_api_key')

        # Sprawdzenie wyniku
        self.assertIsNotNone(result)
        self.assertIn("Request Exception", result)

# ... (inne testy)

if __name__ == '__main__':
    unittest.main()