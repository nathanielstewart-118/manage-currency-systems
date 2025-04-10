from datetime import datetime, timedelta
import requests
import json
import os
serverURL = "https://48v.me/~minifooko/cgi-bin/"
id_path = "id.json"
if os.path.exists(id_path):
    with open(id_path, 'r') as file:
        id_data = json.load(file)
else:
    print("There is no id.json file in the same path.")
    exit()

config_path = 'config.json'

if os.path.exists(config_path):
    flag = True
    with open(config_path, 'r') as file:
        config_data = json.load(file)
else:
    flag = False

print(flag)
# Function to generate a unique MID2
def generate_mid(amount):
    data = {"deposit": amount, "area" : id_data.get('area')}
    
    try:
        # Send a POST request to the server
        response = requests.post(serverURL + "generate_mid_sun.py", data=data)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            print(f"response: {result}")
            mid = result.get("MID")
            sun = result.get("SUN")
            mid_expiry = result.get("MID_expire_date")
            sun_expiry = result.get("SUN_expire_date")
            
            # Display the information
            print(f"New MID: {mid}")
            print(f"SUN: {sun}")
            print(f"MID Expiry: {mid_expiry}")
            print(f"SUN Expiry: {sun_expiry}")
            return mid, sun, mid_expiry, sun_expiry
        else:
            print("Failed to issue MID and SUN. Server responded with:", response.status_code)

    except requests.exceptions.RequestException as e:
        # Handle request errors (e.g., connection issues)
        print(f"Error sending request to server: {e}")

# Deposit funds to a MID
def deposit(mid, deposit_value):
    data = {"deposit": deposit_value, "mid": mid, "area": "atm"}
    try:
        # Send a POST request to the server
        response = requests.post(serverURL + "depositApi.py", data=data)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            print(f"response: {result}")
            message = result.get("message")
        else:
            print("Failed to issue MID and SUN. Server responded with:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Handle request errors (e.g., connection issues)
        print(f"Error sending request to server: {e}")
    return message

# Refund all deposit for the MID
def full_amount_withdrawal(mid):
    data = {"mid": mid,  "area": "atm"}
    try:
        # Send a POST request to the server
        response = requests.post(serverURL + "fullWithdrawalApi.py", data=data)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            print(f"response: {result}")
            message = result.get("message")
        else:
            print("Failed to issue MID and SUN. Server responded with:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Handle request errors (e.g., connection issues)
        print(f"Error sending request to server: {e}")
    return message

# Check if a MID is valid and get the deposit balance
def check_mid(mid):
    data = {"mid": mid,  "area": "atm"}
    try:
        # Send a POST request to the server
        response = requests.post(serverURL + "inquiryApi.py", data=data)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            print(f"response: {result}")
            mid = result.get("MID")
            issue_date = result.get("issue_date")
            deposit = result.get("deposit")
            sun = result.get("SUN")
            sun_expiry = result.get("SUN_expire_date")

            return mid, issue_date, deposit,sun, sun_expiry
        else:
            print("Failed to issue MID and SUN. Server responded with:", response.status_code)
    except requests.exceptions.RequestException as e:
        # Handle request errors (e.g., connection issues)
        print(f"Error sending request to server: {e}")
    
def create_config():
    try:
        url = serverURL + "createConfig.py"
        iddata = {"id" : id_data.get('id'), "area" : id_data.get("area")}
        response = requests.post(url, data=iddata)
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
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

# Main loop for ATM terminal simulation
def main():
    if(flag == False):
        response = create_config()
        # with open(config_path, 'r') as file:
        #     config_data = json.load(file)
        
    while True:
        user_input = input("Enter command (IHAVEMID/HELLOWORLD): ").strip().upper()
        if user_input == "IHAVEMID":
            mid = input("Enter your MID: ").strip()
            user_sec_input = input("Enter command (CONTROLNUMBER/DEPOSIT/RE_ISSUE/REFUND): ").strip().upper()
            if user_sec_input == "controlnumber":  # Replace with your control number
                print("Deleting config.json and rebooting...")
                # Simulate config deletion and reboot
                break
            elif user_sec_input == "DEPOSIT":
                deposit_value = float(input("Enter deposit amount: "))
                
                if deposit_value > 0:
                    response = deposit(mid, deposit_value)
                    print(response)
                else:
                    print("Amount must be greater than 0")

            elif user_sec_input == "RE_ISSUE":
                result = check_mid(mid)
                print(result)

            elif user_sec_input == "REFUND":
                response = full_amount_withdrawal(mid)
                print(response)

        elif user_input == "HELLOWORLD":
            print("New user detected")
            amount = float(input("Enter deposit amount: "))
            if amount > 0:
                mid, sun, mid_expiry, sun_expiry = generate_mid(amount)
                print(f"New MID: {mid}, SUN: {sun}, MID Expiry: {mid_expiry}, SUN Expiry: {sun_expiry}")
            else:
                print("Amount must be greater than 0")

if __name__ == "__main__":
    main()
