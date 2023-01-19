import requests, json, web3
from eth_account import Account
import secrets
import os

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
signed=acct.signHash(challenge_txt)
signed="0"+str(signed)[306:437]
print("-----------")
print(str(signed))
print("-----------")

# get address from wallet
address=str(acct.address)
print("Address:", address)


# get token
headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15"
    }
print("request:",endpoint+get_token+"&challenge="+challenge_txt+"&signature="+signed+"&address="+address)
get = requests.get(endpoint+get_token+"&challenge="+challenge_txt+"&signature="+signed+"&address="+address, headers=headers)
if get.status_code == 200:
    print(get.text)
    #challenge_txt=json.loads(get.text)["challenge"]
else :
    print("token gen error")
    print(get.text)


#notify on LINE

import sys

url = "https://notify-api.line.me/api/notify"
headers = {"Authorization" : "Bearer "+ os.environ["LINE_API"]}
payload = {"message" :  "テストメッセージ：車が見つかりました！"}
r = requests.post(url ,headers = headers ,params=payload)
print(r.text)
