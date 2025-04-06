import logging
from kiteconnect import KiteConnect
import os

logging.basicConfig(level=logging.DEBUG)

api_key = "5gc43yzaypvq7o62"
api_secret = "9ads2gfrt52dm0ycm6brpgxuwuhxcnyc"
access_token_file = "access_token.txt"

kite = KiteConnect(api_key=api_key)

# Load existing access token if available
if os.path.exists(access_token_file):
    with open(access_token_file, "r") as f:
        access_token = f.read().strip()
        kite.set_access_token(access_token)
else:
    # First-time login (manual step required)
    print(kite.login_url())
    request_token = input("Enter request token: ")
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]

    # Save token for reuse during the same day
    with open(access_token_file, "w") as f:
        f.write(access_token)

    kite.set_access_token(access_token)

# Now you can make API calls
print(kite.holdings()[0])