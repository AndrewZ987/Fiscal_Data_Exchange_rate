import requests
import tkinter as tk
from tkinter import ttk

# Define the API endpoint and request parameters
api_endpoint_1 = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange?fields=country_currency_desc,exchange_rate&filter=record_date:eq:2022-12-31&page%5Bnumber%5D=1&page%5Bsize%5D=100"
api_endpoint_2 = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange?fields=country_currency_desc,exchange_rate&filter=record_date:eq:2022-12-31&page%5Bnumber%5D=2&page%5Bsize%5D=100"
params = {
    "fields": "country_currency_desc,exchange_rate",
    "filter": "record_date:eq:2022-12-31"
}

try:
    # Send the GET request
    response_1 = requests.get(api_endpoint_1, params=params)
    response_2 = requests.get(api_endpoint_2, params=params)
    # Check if the request was successful (status code 200)
    if response_1.status_code == 200:
        # Parse the JSON response
        data_1 = response_1.json()
        data_2 = response_2.json()

        # Create a Tkinter window
        root = tk.Tk()
        root.title("Currency Converter")

        date_label = ttk.Label(root, text="Currently Date Selected : 2022/12/31")
        date_label.pack(padx=10, pady=10)

        # Create a label
        label = ttk.Label(root, text="Select a country currency:")
        label.pack(padx=10, pady=10)

        # Create a drop-down list
        currency_var = tk.StringVar()
        currency_combo = ttk.Combobox(root, textvariable=currency_var)
        
        # Extract and populate the currency data in the drop-down list
        exchange_rate_data1 = data_1.get("data", [])
        exchange_rate_data2 = data_2.get("data", [])
        # print(type(exchange_rate_data1))
        currencies = set()
        for entry in exchange_rate_data1:
            currency = entry.get("country_currency_desc", "N/A")
            exchange_rate = entry.get("exchange_rate", "N/A")
            currencies.add((currency, exchange_rate))

        for entry in exchange_rate_data2:
            currency = entry.get("country_currency_desc", "N/A")
            exchange_rate = entry.get("exchange_rate", "N/A")
            currencies.add((currency, exchange_rate))

        currency_list = sorted(currencies, key=lambda x: x[0])
        currency_names = [item[0] for item in currency_list]
        currency_combo["values"] = currency_names
        currency_combo.pack(padx=10, pady=10)

        # Function to perform the conversion
        def convert_currency():
            selected_currency = currency_var.get()
            for entry in currency_list:
                if entry[0] == selected_currency:
                    exchange_rate_label.config(text=f"Exchange Rate: {entry[1]}")
                    exchange_rate = float(entry[1])
                    try:
                        amount = float(amount_entry.get())
                        usd_amount = amount / exchange_rate
                        result_label.config(text=f"{amount:.2f} {selected_currency} is equivalent to {usd_amount:.2f} USD")
                    except ValueError:
                        result_label.config(text="Invalid input. Please enter a valid number.")
                    break

        # Create a label and entry for user input
        amount_label = ttk.Label(root, text="Enter an amount:")
        amount_label.pack(padx=10, pady=5)
        amount_entry = ttk.Entry(root)
        amount_entry.pack(padx=10, pady=5)

        # Create a button to perform the conversion
        convert_button = ttk.Button(root, text="Convert", command=convert_currency)
        convert_button.pack(padx=10, pady=10)

        # Create a label to display the exchange rate
        exchange_rate_label = ttk.Label(root, text="")
        exchange_rate_label.pack(padx=10, pady=10)
        result_label = ttk.Label(root, text="")
        result_label.pack(padx=10, pady=10)

        # Start the Tkinter main loop
        root.mainloop()
    else:
        print(f"Request failed with status code: {response_1.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred during the request: {str(e)}")
