import random
from datetime import datetime, timedelta
import requests
import json
import os

serverURL = "https://48v.me/~minifooko/cgi-bin/"

id_path = "id.json"
with open(id_path, 'r') as file:
    id_data = json.load(file)

config_path = 'config.json'
if os.path.exists(config_path):
    flag = True
    with open(config_path, 'r') as file:
        config_data = json.load(file)
else:
    flag = False

# Function to process a service request (contact the server)
def process_service(sun, service_type, service_price, contact_id):
    # Timestamp for the service request
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Simulate sending a command to the server
    print(f"Sending command: 'contact' with SUN {sun}, service_type {service_type}, service_price {service_price}, contact_id {contact_id}, timestamp {timestamp}")
    
    if service_type == "IMMEDIATE":
        message, remain = simulate_server_response_immediate(sun, service_price, service_type)
        if message == "No deposit":
            print(f"No deposit")
            return
        elif message == "Thank you":
            print(f"Thank you. Remaining balance: {remain}")
            return
        else:
            # store_command(sun, service_type, service_price, timestamp, contact_id)
            print("Service request stored for later.")

    elif service_type == "PAYAFTERSERVICE":
        response = simulate_server_response_payafterservice(sun, service_price, service_type)
        if response == "no deposit":
            print("No deposit")
            return
        elif response == "thankyou":
            print("Thank you.")
            user_input = input("Input 'done' to finalize or 'cancel' to cancel: ")
            if user_input == "done":
                invoice_command(contact_id, sun, service_price)
            elif user_input == "cancel":
                cancel_invoice(contact_id, sun)
        else:
            print("Service request stored for later.")

def simulate_server_response_immediate(sun, service_price, service_type):
    data = {"sun": sun, "deposit_value": service_price, "service_type": service_type, "area": "service"}
    try:
        response = requests.post(serverURL + "contactApi.py", data=data)
        result = response.json()
        print(f"result: {result}")
        if response.status_code == 200:
            return result.get("message"), result.get("remain")
        else:
            result = response.json()
            return result.get("message"), 0

    except requests.exceptions.RequestException as e:
        print(f"Error sending request to server: {e}")

def simulate_server_response_payafterservice(sun, service_price, service_type):
    data = {"sun": sun, "deposit_value": service_price, "service_type": service_type, "area": "service"}
    print(data)
    try:
        response = requests.post(serverURL + "contactApi.py", data=data)

        print(response.status_code)
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            print(f"result: {result}") 
        else:
            result = response.json()
            print(f"result: {result}") 

    except requests.exceptions.RequestException as e:
        print(f"Error sending request to server: {e}")

# def store_command(sun, service_type, service_price, timestamp, contact_id):
#     connection = db_connection()
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO service_commands (SUN, service_type, service_price, timestamp, processed) VALUES (%s, %s, %s, %s, %s)",
#                    (sun, service_type, service_price, timestamp, False))
#     connection.commit()
#     cursor.close()
#     connection.close()

# Function to send an invoice command
def invoice_command(contact_id, sun, service_price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Sending invoice command: 'invoice' with contact_id {contact_id}, SUN {sun}, service_price {service_price}, timestamp {timestamp}")
    response = simulate_server_response_invoice(sun)
    if response == "OK":
        print(f"Invoice sent successfully. Remaining balance: {get_remaining_balance(sun)}")
    else:
        # store_command(sun, "PAYAFTERSERVICE", service_price, timestamp, contact_id)
        print("Invoice command stored for later.")

# Simulate the server's response to an invoice command
def simulate_server_response_invoice(sun):
    # In a real implementation, server interaction happens here
    # For simulation, return "OK"
    return "OK"

# Function to send a cancel invoice command
def cancel_invoice(contact_id, sun):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Sending cancel command: 'cancelinvoice' with contact_id {contact_id}, SUN {sun}, timestamp {timestamp}")
    response = simulate_server_response_cancel(sun)
    if response == "OK":
        print(f"Invoice canceled successfully. Remaining balance: {get_remaining_balance(sun)}")
    else:
        # store_command(sun, "PAYAFTERSERVICE", 300, timestamp, contact_id)
        print("Cancel invoice command stored for later.")

# Simulate the server's response to cancel an invoice
def simulate_server_response_cancel(sun):
    # In a real implementation, server interaction happens here
    # For simulation, return "OK"
    return "OK"

# Function to get the remaining balance for a MID (simulated)
def get_remaining_balance(sun):
    # In a real implementation, get the MID associated with the SUN
    # Here we simulate it and return a random balance
    return random.randint(10, 1000)

def create_config():
    try:
        url = serverURL + "createConfig.py"
        iddata = {"id" : id_data.get('id'), "area" : id_data.get("area")}
        response = requests.post(url, data=iddata)
        print(response)
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            print(result)
            output_directory = "./"
            output_file = "config.json"
            output_path = os.path.join(output_directory, output_file)
            os.makedirs(output_directory, exist_ok=True)
            try:
                with open(output_path, "w") as json_file:
                    json.dump(result, json_file, indent=4)  # Write JSON data with pretty formatting
                return "success"
            except Exception as e:
                print(f"Failed to create the file: {e}")
        else:
            print("Failed to issue MID and SUN. Server responded with:", response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while downloading the file: {e}")
# Main loop for the Service Terminal
def main():
    if(flag == False):
        response = create_config()
        
    while True:
        sun = input("Enter SUN: ").strip()
        service_type = input("Enter service type (IMMEDIATE/PAYAFTERSERVICE): ").strip()
        service_price = input("Enter service price: ").strip()  # Assume fixed service price
        contact_id = random.randint(1, 9999)  # Generate a unique contact ID
        process_service(sun, service_type, service_price, contact_id)

if __name__ == "__main__":
    main()
