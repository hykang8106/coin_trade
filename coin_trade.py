# coin trade using "Upbit Client"
# 
# Upbit Client Official Reference
#
# https://ujhin.github.io/upbit-client-docs/#upbit-client-official-reference
#
# install "Upbit Client":
# "pip install upbit-client"
#
# another useful reference:
# (1) https://docs.upbit.com/docs
# (2) https://wikidocs.net/book/1665 파이썬을 이용한 비트코인 자동매매 (개정판)
#
# [visual studio code keyboard shortcut]
# toggle block comment: shift + alt + a
# toggle line comment: ctrl + /
#
# whenever power on computer, 
# (1) get computer ip address using "ipconfig" command(internet provider assign ip address in random way).
# (2) log in upbit web site, and get registered ip address in upbit api.
#     (https://upbit.com/mypage/open_api_management)
#     (log in require upbit katalk authentication code)
# (3) if registered ip address is not same as computer ip address, 
#     registered ip address must be changed to computer ip address.
#     change is bothering because authentication process is required.
#     kakaopay authentication code = uresj35805
#
# computer ip address example:
# 222.233.84.163
# 114.203.170.28
# 175.124.98.245
# 61.101.9.104
# 39.119.56.140(current)
#

import sys
import json
from numpy import mean
from upbit.client import Upbit

access_key = "six3Lna2c62lyVxEP2NtJRKd0Um1Wme84hLrLMGl"
secret_key = "9X2fJx3g7nr3hGEyxLnfFx7Fl6sMNxypccbkSxy8"
# key expire at 2023.05.03

# json.load: read json data from file
# json.loads: convert json string to python dictionary
# json.dump: save python dictionary into file
# json.dumps: convert python dictionary to json string
def print_json(resp):

    print(json.dumps(resp, indent=3, default=str))

# pseudo code
""" 
[single trading algorithm]

start program
if buy history file exist
    load buy price and volume from file
    enter loop to query current price
    if current price is 15% more than buy price
        sell(ask) coin by volume loaded from file
        remove buy history file
        exit loop
    else
        continue loop
else
    if command argument have buy price
        set it to initial price
    else
        query candle price(two week/month, open price, close price, high price, low price)
        compute averaged price, and set it into initial price
    enter loop to query current price
    if current price is 10% less than initial price
        buy(bid) coin
        create buy history file
        save buy price and volume into buy history file
        exit loop
    else
        continue loop
stop program
"""

# ask: sell, bid: buy
#
##########################################
# important and hard question: when to bid(buy), when to ask(sell)
#########################################

#############################
# my coin: ETH, ADA, DOGE
#
# code focus is on DOGE
# 
# [ask/bid] fee: 0.0005, maker fee: 0.0005, total fee(= fee + maker fee): 0.001
#
# [ask/bid minimum price] 5000 KRW
#############################

# 클라이언트 객체 생성
client = Upbit(access_key, secret_key)
# print(client)

# 마켓별 주문 가능 정보를 확인합니다.
resp = client.Order.Order_chance(
    market='KRW-DOGE'
)
print_json(resp['result'])

# 현재 시세 호가 정보를 조회합니다.
resp = client.Order.Order_orderbook(
    markets=['KRW-DOGE']
)
print_json(resp['result'])

# 최근 체결 내역을 조회합니다.
resp = client.Trade.Trade_ticks(
    market='KRW-DOGE',
    count=2
)
print_json(resp['result'])

# 요청 당시 종목의 스냅샷을 반환합니다.
resp = client.Trade.Trade_ticker(
    markets='KRW-DOGE'
)
print_json(resp['result'])
print(resp['result'][0]['trade_price'])

candle_count = 2

# 주(Week) 단위로 시세 캔들을 조회합니다.
resp = client.Candle.Candle_weeks(
    market='KRW-DOGE',
    count=candle_count
)
print_json(resp['result'])

# 월(Month) 단위로 시세 캔들을 조회합니다.
resp = client.Candle.Candle_month(
    market='KRW-DOGE',
    count=candle_count
)
print_json(resp['result'])




