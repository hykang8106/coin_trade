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
# ask: sell, bid: buy
#
# [visual studio code keyboard shortcut]
# toggle block comment: shift + alt + a
# toggle line comment: ctrl + /
#
# whenever power on computer, 
# (1) get computer ip address using "ipconfig" command(internet provider assign ip address in random way).
# (2) log in upbit web site, and get registered ip address in upbit api.
#     (https://upbit.com/mypage/open_api_management)
# (3) if registered ip address is not same as computer ip address, 
#     registered ip address must be changed to computer ip address.
#     change is bothering because authentication process is required.
#     kakaopay authentication code = uresj35805
#
# computer ip address example:
# 222.233.84.163(current)
# 114.203.170.28
# 175.124.98.245
# 61.101.9.104
#

# pseudo code

""" 
query current value, and save it into initial value
enter for loop to query current value
if current value is 10% less than initial value
buy(bid) coin
else if current value is 10% more than initial value
sell(ask) coin
else
continue to for loop
"""

import sys
import json
from upbit.client import Upbit

access_key = "six3Lna2c62lyVxEP2NtJRKd0Um1Wme84hLrLMGl"
secret_key = "9X2fJx3g7nr3hGEyxLnfFx7Fl6sMNxypccbkSxy8"

# json.load: read json data from file
# json.loads: convert json string to python dictionary
# json.dump: save python dictionary into file
# json.dumps: convert python dictionary to json string
def print_json(resp):

    print(json.dumps(resp, indent=3, default=str))


# pretty print dictionary
# ref: https://stackoverflow.com/questions/3229419/how-to-pretty-print-nested-dictionaries
def print_dict(resp, indent=0):

    for key, value in resp.items():
        print('  ' * indent + str(key))
        if isinstance(value, dict):
            print_dict(value, indent + 1)
        else:
            print('  ' * (indent + 1) + str(value))

# 클라이언트 객체 생성
client = Upbit(access_key, secret_key)
print(client)

# API 키 리스트 조회
# API 키 목록 및 만료 일자를 조회합니다.
resp = client.APIKey.APIKey_info()
print_json(resp)
# print_dict(resp)
# print(resp['result'])
print_json(resp['result'])

# sys.exit()

# 전체 계좌 조회
# 내가 보유한 자산 리스트를 보여줍니다.
resp = client.Account.Account_info()
# print(resp['result'])
print_json(resp['result'])

# 입출금 현황
# 입출금 현황 및 블록 상태를 조회합니다.
resp = client.Account.Account_wallet()
# print(resp['result'])
print_json(resp['result'])

# 마켓 코드 조회
# 업비트에서 거래 가능한 마켓 목록을 조회합니다.
resp = client.Market.Market_info_all()
# print(resp['result'])
print_json(resp['result'])

# 현재 시세 호가 정보를 조회합니다.
resp = client.Order.Order_orderbook(
    markets=['KRW-BTC', 'KRW-ETH']
)
# print(resp['result'])
print_json(resp['result'])
#### below comment out due to error: "AttributeError: 'list' object has no attribute 'items'"
# print_dict(resp['result'])

# 마켓별 주문 가능 정보를 확인합니다.
resp = client.Order.Order_chance(
    market='KRW-BTC'
)
print_json(resp['result'])

# 주문 UUID 를 통해 개별 주문건을 조회합니다.
#########################################
# must run after learning
#########################################
""" resp = client.Order.Order_info(
    uuid='9ca023a5-851b-4fec-9f0a-48cd83c2eaae'
)
print(resp['result']) """

# 주문 리스트를 조회합니다.
resp = client.Order.Order_info_all()
print_json(resp['result'])

# sys.exit()

# 새로운 주문 요청을 합니다.
# 새로운 주문을 하개 되면, 응답으로 uuid 값이 돌아옴. 이 값은 주문 취소에 사용할 수 있음.
#########################################
# must run after learning
#########################################
""" resp = client.Order.Order_new(
    market='KRW-BTC',
    side='bid',
    volume='0.01',
    price='100.0',
    ord_type='limit'
)
print(resp['result']) """

# 주문 UUID를 통해 해당 주문에 대한 취소 접수를 합니다.
#########################################
# must run after learning
#########################################
""" resp = client.Order.Order_cancel(
    uuid='cdd92199-2897-4e14-9448-f923320408ad'
)
print(resp['result']) """

# 입금 리스트 조회합니다.
resp = client.Deposit.Deposit_info_all()
print_json(resp['result'])

# sys.exit()

# 개별 입금 내역을 조회합니다.
#########################################
# must run after learning
#########################################
""" resp = client.Deposit.Deposit_info(
    uuid='20c84493-6e70-4e54-83ce-90915a19d110'
)
print(resp['result']) """

# 내가 보유한 자산 리스트를 보여줍니다.
resp = client.Deposit.Deposit_coin_addresses()
print_json(resp['result'])

# sys.exit()

# 내가 보유한 개별 자산 내역을 보여줍니다.
#########################################
# must run after learning
#########################################
""" resp = client.Deposit.Deposit_coin_address(
    currency='BTC'
)
print(resp['result']) """

# 입금 주소 생성을 요청합니다.
#########################################
# must run after learning
#########################################
""" resp = client.Deposit.Deposit_generate_coin_address(
    currency='SNT'
)
print(resp['result']) """

# 출금 리스트 조회합니다.
#########################################
# 출금 코인 주소가 등록되어 있지않으므로, return 값이 없음.
#########################################
resp = client.Withdraw.Withdraw_info_all()
print_json(resp['result'])

# sys.exit()

# 출금 UUID를 통해 개별 출금 정보를 조회합니다.
#########################################
# must run after learning
#########################################
""" resp = client.Withdraw.Withdraw_info(
    uuid='35a4f1dc-1db5-4d6b-89b5-7ec137875956'
)
print(resp['result']) """

# 해당 통화의 가능한 출금 정보를 확인합니다.
#########################################
# must run after learning
#########################################
""" resp = client.Withdraw.Withdraw_chance(
    currency='BTC'
)
print(resp['result']) """

# 코인 출금을 요청합니다.
#########################################
# must run after learning
#########################################
""" resp = client.Withdraw.Withdraw_coin(
    currency='BTC',
    amount='0.01',
    address='3NVw2seiTQddGQwc1apqudKxuTqebpyL3s'
)
print(resp['result']) """

# 원화 출금 요청을 합니다. 등록된 출금 계좌로 출금됩니다.
#########################################
# must run after learning
#########################################
""" resp = client.Withdraw.Withdraw_krw(
    amount='10000'
)
print(resp['result']) """

# 분(Miniute) 단위로 시세 캔들을 조회합니다.
resp = client.Candle.Candle_minutes(
    unit=1,
    market='KRW-BTC'
)
print_json(resp['result'])

# 일(Day) 단위로 시세 캔들을 조회합니다.
resp = client.Candle.Candle_days(
    market='KRW-BTC'
)
print_json(resp['result'])

# 주(Week) 단위로 시세 캔들을 조회합니다.
resp = client.Candle.Candle_weeks(
    market='KRW-BTC'
)
print_json(resp['result'])

# 월(Month) 단위로 시세 캔들을 조회합니다.
resp = client.Candle.Candle_month(
    market='KRW-BTC'
)
print_json(resp['result'])

# sys.exit()

# 최근 체결 내역을 조회합니다.
resp = client.Trade.Trade_ticks(
    market='KRW-BTC'
)
print_json(resp['result'])

# 요청 당시 종목의 스냅샷을 반환합니다.
resp = client.Trade.Trade_ticker(
    markets='KRW-BTC, KRW-ETH'
)
print_json(resp['result'])


























