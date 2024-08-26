import unittest
from unittest.mock import patch, MagicMock
import requests
import sys

# Import the functions from the main script
from your_script_name import fetch_data, parse_data, display_information

class TestCryptoFetcher(unittest.TestCase):

    @patch('your_script_name.requests.get')
    def test_fetch_data_success(self, mock_get):
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "time": {"updated": "Oct 9, 2023 00:03:00 UTC"},
            "bpi": {"GBP": {"rate": "24,000.0000"}}
        }
        mock_get.return_value = mock_response

        api_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        data = fetch_data(api_url)
        
        self.assertIn('time', data)
        self.assertIn('bpi', data)
        self.assertEqual(data['bpi']['GBP']['rate'], "24,000.0000")

    @patch('your_script_name.requests.get')
    def test_fetch_data_timeout(self, mock_get):
        # Mock a timeout scenario
        mock_get.side_effect = requests.exceptions.Timeout
        api_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        
        with self.assertRaises(SystemExit):
            fetch_data(api_url)

    @patch('your_script_name.requests.get')
    def test_fetch_data_connection_error(self, mock_get):
        # Mock a connection error scenario
        mock_get.side_effect = requests.exceptions.ConnectionError
        api_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        
        with self.assertRaises(SystemExit):
            fetch_data(api_url)

    def test_parse_data_success(self):
        # Mock data as it would be returned from the API
        mock_data = {
            "time": {"updated": "Oct 9, 2023 00:03:00 UTC"},
            "bpi": {"GBP": {"rate": "24,000.0000"}}
        }
        updated_time, currency_rate = parse_data(mock_data, "GBP")
        self.assertEqual(updated_time, "Oct 9, 2023 00:03:00 UTC")
        self.assertEqual(currency_rate, "24,000.0000")

    def test_parse_data_key_error(self):
        # Mock data missing the expected keys
        mock_data = {"time": {"updated": "Oct 9, 2023 00:03:00 UTC"}}
        
        with self.assertRaises(SystemExit):
            parse_data(mock_data, "GBP")

    def test_display_information(self):
        # Capture the output of the display_information function
        updated_time = "Oct 9, 2023 00:03:00 UTC"
        currency_rate = "24,000.0000"
        currency = "GBP"

        # Test output using a context manager to capture stdout
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            display_information(updated_time, currency_rate, currency)
            output = mock_stdout.getvalue()

        self.assertIn("Information as of: Oct 9, 2023 00:03:00 UTC", output)
        self.assertIn("GBP Rate: 24,000.0000", output)

if __name__ == '__main__':
    unittest.main()
