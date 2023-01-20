import requests, json, web3
from web3.auto import w3
from eth_account import Account
import secrets
import os
from eth_account.messages import encode_defunct

endpoint = 'https://us-central1-carshare-naist-dev.cloudfunctions.net/api'
challenge = "?auth=challenge"
get_token = "?auth=accesstoken"
getlocation = "?method=getLocations"

# get challenge
headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    }
get = requests.get(endpoint+challenge, headers=headers)
challenge_txt=""
if get.status_code == 200:
    challenge_txt=json.loads(get.text)["challenge"]
    print("challenge:",challenge_txt)
else :
    print("challenge error")

#generate random wallet
priv = secrets.token_hex(32)
private_key = "0x" + priv
print ("SAVE BUT DO NOT SHARE THIS:", private_key)
acct = Account.from_key(private_key)

      
# get signature from wallet
signed_=w3.eth.account.sign_message(encode_defunct(text=challenge_txt), private_key=priv)
print("-----------")
print(str(signed_))
print("----")
print(str(signed_)[-136:-4])
print("-----------")
signed=str(signed_)[-136:-4]

# get address from wallet
address=str(acct.address)
print("Address:", address)


# get token
headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
    }
print("request:",endpoint+get_token+"&challenge="+challenge_txt+"&signature="+signed+"&address="+address)
"""
get = requests.get(endpoint+get_token+"&challenge="+challenge_txt+"&signature="+signed+"&address="+address, headers=headers)

token=""
if get.status_code == 200:
    print("accessed:",get.text)
    token=json.loads(get.text)["token"]
else :
    print("token gen error")
    print(get.text)
    
#get geo
headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Authorization": "Bearer "+token
    }

print(headers)
get = requests.get(endpoint+getlocation, headers=headers)

if get.status_code == 200:
    print("geo:",get.text)
else :
    print("token acess error")
    print(get.text)
    

#notify on LINE

import sys

url = "https://notify-api.line.me/api/notify"

headers = {"Authorization" : "Bearer "+ os.environ.get("LINE_API")}
payload = {"message" :  "テストメッセージ：車が見つかりました！"}
#r = requests.post(url ,headers = headers ,params=payload)
#print(r.text)
"""
