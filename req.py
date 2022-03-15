import requests
from getmac import get_mac_address as gma

URL = "https://amazon.quantrecenergy.in/api/get_mac.php"
system_mac = gma().strip()

system_mac = system_mac.replace("-", ":")
system_mac = system_mac.lower()

name = input("Enter your Name\n")

PARAMS = {'mac':system_mac, 'name':name}
r = requests.post(URL, PARAMS)
auth = r.text

if auth == "true":
    print("Your registration key successfully genrate")
else:
    print("Your registration key not genrate")

input("\n\n\n========================= Press Enter  to exit ============================")
