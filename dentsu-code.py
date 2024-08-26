import requests
import sys
import json
import argparse

def fetch_data(api_url):
    """
    Fetches the data from the specified API URL.
    """
    try:
        response = requests.get(api_url, timeout=10)  # Set a timeout for the request
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please check your network connection or try again later.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API. Please check your network connection.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.reason}. Please check the API endpoint and try again.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: An unexpected error occurred while trying to fetch data: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to decode the JSON response. The API may have changed its response format.")
        sys.exit(1)

def parse_data(data, currency):
    """
    Parses the JSON data to extract the updated time and the currency rate.
    """
    try:
        updated_time = data['time']['updated']
        currency_rate = data['bpi'][currency]['rate']
        return updated_time, currency_rate
    except KeyError as e:
        print(f"Error: The expected data format is missing key: {e}. The API response may have changed.")
        sys.exit(1)

def display_information(updated_time, currency_rate, currency):
    """
    Displays the extracted information on the screen with clear labels.
    """
    print(f"Information as of: {updated_time}")
    print(f"{currency} Rate: {currency_rate}")

def main(api_url, currency):
    """
    Main function to fetch, parse, and display the data.
    """
    data = fetch_data(api_url)
    updated_time, currency_rate = parse_data(data, currency)
    display_information(updated_time, currency_rate, currency)

if __name__ == "__main__":
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Fetch and display cryptocurrency rates.')
    parser.add_argument('--api_url', type=str, default='https://api.coindesk.com/v1/bpi/currentprice.json', help='The API endpoint URL')
    parser.add_argument('--currency', type=str, default='GBP', choices=['USD', 'GBP', 'EUR'], help='The currency code (USD, GBP, EUR)')
    
    args = parser.parse_args()

    # Run the main function
    main(args.api_url, args.currency)
