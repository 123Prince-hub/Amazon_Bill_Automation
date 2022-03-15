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










# import random
# import base64
# from Crypto.Cipher import AES

# rand_num = random.randint(100000, 999999)
# rand_num = str(rand_num)+"aaaaaaaa"

# secret_key = b'1121121121121212'

# msg_text = rand_num+"@"+system_mac
# msg_text = msg_text.encode().rjust(32)

# cipher = AES.new(secret_key,AES.MODE_ECB) # never use ECB in strong systems obviously

# encoded = base64.b64encode(cipher.encrypt(msg_text))
# print(encoded)

# decoded = cipher.decrypt(base64.b64decode(encoded))
# print(decoded)

