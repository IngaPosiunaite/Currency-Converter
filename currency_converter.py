import requests
from pprint import PrettyPrinter

class CurrencyConverter:
    """
    A class to handle currency conversion using an API.
    
    Attributes:
        api_key (str): The API key for accessing the currency conversion API.
        printer (PrettyPrinter): An instance of PrettyPrinter for printing formatted output.
    """
    BASE_URL = "https://free.currconv.com/"
    
    def __init__(self, api_key):
        """
        Initializes the CurrencyConverter with the API key.
        
        Args:
            api_key (str): The API key for accessing the currency conversion API.
        """
        self.api_key = api_key
        self.printer = PrettyPrinter()
    
    def _make_request(self, endpoint):
        """
        Makes a request to the API and returns the JSON response.
        
        Args:
            endpoint (str): The API endpoint to request data from.
            
        Returns:
            dict: The JSON response from the API.
            
        Raises:
            Exception: If the API request fails or returns an unexpected status code.
        """
        url = f"{self.BASE_URL}{endpoint}&apiKey={self.api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from API. Status code: {response.status_code}")
        return response.json()
    
    def get_currencies(self):
        """
        Retrieves a list of available currencies from the API.
        
        Returns:
            list: A list of tuples containing currency codes and names.
        """
        data = self._make_request("api/v7/currencies?")
        currencies = list(data['results'].items())
        currencies.sort()
        return currencies
    
    def print_currencies(self, currencies):
        """
        Prints a formatted list of currencies.
        
        Args:
            currencies (list): A list of tuples containing currency codes and names.
        """
        for name, currency in currencies:
            name = currency['currencyName']
            _id = currency['id']
            symbol = currency.get("currencySymbol", "")
            print(f"{_id} - {name} - {symbol}")
    
    def exchange_rate(self, currency1, currency2):
        """
        Retrieves the exchange rate between two currencies.
        
        Args:
            currency1 (str): The base currency code.
            currency2 (str): The target currency code.
            
        Returns:
            float: The exchange rate from currency1 to currency2.
        """
        data = self._make_request(f"api/v7/convert?q={currency1}_{currency2}&compact=ultra")
        rate = list(data.values())[0]
        print(f"{currency1} -> {currency2} = {rate}")
        return rate
    
    def convert(self, currency1, currency2, amount):
        """
        Converts an amount from one currency to another.
        
        Args:
            currency1 (str): The base currency code.
            currency2 (str): The target currency code.
            amount (str): The amount to convert.
            
        Returns:
            float: The converted amount.
        """
        rate = self.exchange_rate(currency1, currency2)
        if rate is None:
            return
        
        try:
            amount = float(amount)
        except ValueError:
            print("Invalid amount.")
            return
        
        converted_amount = rate * amount
        print(f"{amount} {currency1} is equal to {converted_amount} {currency2}")
        return converted_amount

def main():
    """
    The main function to run the currency converter application.
    """
    api_key = "562ddaf40c95f5d58108"  # Replace with your API key
    converter = CurrencyConverter(api_key)

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            currencies = converter.get_currencies()
            converter.print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            amount = input(f"Enter an amount in {currency1}: ")
            currency2 = input("Enter a currency to convert to: ").upper()
            converter.convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            converter.exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")

if __name__ == "__main__":
    main()