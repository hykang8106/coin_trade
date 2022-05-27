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
# unindent block: shift + tab
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
# desktop ip address example:
# 222.233.84.163
# 114.203.170.28
# 175.124.98.245
# 61.101.9.104
# 39.119.56.140
# 218.49.178.21(registered)
# 123.215.35.19
#
# macbook ip address example:
# 172.16.11.207

###################################################################
# ask: sell, bid: buy
#
# important and hard question: when to bid(buy), when to ask(sell)
###################################################################

################################################################################
# my coin: ETH, ADA, DOGE
#
# code is for DOGE
# 
# [ask/bid] fee: 0.0005, maker fee: 0.0005, total fee(= fee + maker fee): 0.001
#
# [ask/bid minimum price] 5000 KRW
################################################################################

###########################################################################################
# command usage: 
# doge_trade market averge_unit unit_count buy_margin_percent sell_margin_percent buy_krw
# command example: 
# doge_trade KRW-DOGE day 3 -2 3 6000
###########################################################################################

import sys
import json
from os.path import exists
import time
from numpy import mean
import os
from datetime import datetime

from upbit.client import Upbit

program_test = True

###############################################################
# market: one of "KRW-BTC", "KRW-ETH", "KRW-DOGE", "KRW-ADA"
###############################################################
market_list = ["KRW-BTC", "KRW-ETH", "KRW-DOGE", "KRW-ADA"]

file_list = ["buy_try.txt", "buy_done.txt", "sell_try.txt", "sell_done.txt"]

# buy_file = "buy.txt"

# average_unit: one of "minute", "day", "week", "month"
average_unit_list = ["minute", "day", "week", "month"]

# for loop count limit
loop_count = 2**10

# current price query interval(5 min)
sleep_sec = 5 * 60

""" # buy when current price is 3% lower than initial price(i.e. two days averaged price)
buy_margin_percent = 3
# sell when current price is 1% higher than buy price
sell_margin_percent = 1 """

buy_min_krw = 6000
sell_min_krw = 6000

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
# 
# [main flow]
# 
# (0) start trade session
# (1) check current price to buy
# (2) order buy when good price, and create buy try file
# (3) check buy order result
# (4) when buy done, rename buy try file to buy done file
# (5) check current price to sell
# (6) order sell when good price, remove buy done file, and create sell try file
# (7) check sell order result
# (8) when sell done, rename sell try file to sell done file
# (9) prepend time stamp to sell done file name
# (10) restart new session

""" 
get market name from command argument
enter loop to check file exist
    if buy done file exist
        load price and volume from buy done file
        enter loop to query current price
            if current price is 15% more than buy price
                try to sell(ask) coin for price and volume
                keep uuid from order response
                remove buy done file
                create sell try file
                save sell price, volume, and uuid into sell try file
                exit loop
            else
                sleep
                continue loop
    else if buy try file exist
        load price, volume, and uuid from buy try file
        enter loop to query buy status for uuid
            if buy status is done
                rename buy try file to buy done file
                exit loop
            else
                sleep
                continue loop
    else if sell try file exist
        load price, volume, and uuid from sell try file
        enter loop to query sell status for uuid
            if sell status is done
                rename sell try file to sell done file
                prepend timestamp to sell done filename(sell history file)
                exit loop
            else
                sleep
                continue loop
    else (no file exist)
        if command argument have buy price
            set it to initial price
        else
            query candle price(two week/month, open price, close price, high price, low price)
            compute averaged price, and set it into initial price
        enter loop to query current price
            if current price is 10% less than initial price
                try to buy(bid) coin for price and volume
                keep uuid from order response
                create buy try file
                save buy price, volume, and uuid into buy try file
                exit loop
            else
                sleep
                continue loop
"""

def timestamp_sell_done(market):

    sell_done_file = market + "_" + file_list[3]
    now_str = datetime.now().strftime("%y%m%d%H%M%S")
    os.rename(sell_done_file, now_str + "_" + sell_done_file)

def get_averaged_price(client, market, average_unit, unit_count):

    if average_unit == "minute":
        # 분(Miniute) 단위로 시세 캔들을 조회합니다.
        resp = client.Candle.Candle_minutes(
            market=market,
            count=unit_count
        )

    elif average_unit == "day":
        # 주(Week) 단위로 시세 캔들을 조회합니다.
        resp = client.Candle.Candle_days(
            market=market,
            count=unit_count
        )
        
    elif average_unit == "week":
        # 주(Week) 단위로 시세 캔들을 조회합니다.
        resp = client.Candle.Candle_weeks(
            market=market,
            count=unit_count
        )

    else:
        # 월(Month) 단위로 시세 캔들을 조회합니다.
        resp = client.Candle.Candle_month(
            market=market,
            count=unit_count
        )

    # print_json(resp['result'])   

    # average opening_price, trade_price for each candle, and again average "unit_count" candle
    reference_price = mean([(y['opening_price'] + y['trade_price'])/2 for y in resp['result']])

    return reference_price

def load_price_and_volume(trade_file):

    with open(trade_file, "r") as f:
        uuid, price, volume = f.read().rstrip("\n").split(",")

        f.close()

    return uuid, price, volume

def buy_coin(client, market, buy_price, buy_volume):

    resp = client.Order.Order_new(
        market=market,
        side='bid',
        volume=str(buy_volume),
        price=str(buy_price),
        ord_type='limit'
    )
    print_json(resp['result'])

    # check buy result
    #### code here

    buy_uuid = resp['result']['uuid']

    return buy_uuid

def sell_coin(client, market, sell_price, sell_volume):

    resp = client.Order.Order_new(
        market=market,
        side='ask',
        volume=str(sell_volume),
        price=str(sell_price),
        ord_type='limit'
    )
    print_json(resp['result'])

    # check sell result
    #### code here

    sell_uuid = resp['result']['uuid']

    return sell_uuid

def sell_status_loop(client, market):

    """ 
    load uuid, price, volume from sell try file
    enter loop to query sell status for uuid
        if sell status is done
            rename sell try file to sell done file
            prepend timestamp to sell done filename(sell history file)
            exit loop
        else
            sleep
            continue loop 
    """

    # file_list = ["buy_try.txt", "buy_done.txt", "sell_try.txt", "sell_done.txt"]
    market_sell_try_file = market + "_" + file_list[2]

    sell_uuid, sell_price, sell_volume = load_price_and_volume(market_sell_try_file)

    for x in range(loop_count):

        if program_test:
            state = "done"
        else:
            resp = client.Order.Order_info(
                uuid=sell_uuid
            )
            print_json(resp['result'])
            state = resp['result']['state']

        if state == "done":
            # rename buy try file to buy done file
            market_sell_done_file = market + "_" + file_list[3]
            os.rename(market_sell_try_file, market_sell_done_file)
            break
        else:
            time.sleep(sleep_sec)
            continue
    
    if x == (loop_count - 1):
        print("#### sell status count end")

    pass

def sell_try_loop(client, market, sell_margin_percent):

    """ 
    load uuid, price, volume from buy done file
    enter loop to query current price
        if current price is 15% more than buy price
            order to sell(ask) coin for price and volume
            keep uuid from order response
            remove buy done file
            create sell try file
            save sell uuid, price, volume into sell try file
            exit loop
        else
            sleep
            continue loop
    """

    # file_list = ["buy_try.txt", "buy_done.txt", "sell_try.txt", "sell_done.txt"]
    market_buy_done_file = market + "_" + file_list[1]

    buy_uuid, buy_price, buy_volume = load_price_and_volume(market_buy_done_file)

    for x in range(loop_count):

        # get current price
        # 요청 당시 종목의 스냅샷을 반환합니다.
        resp = client.Trade.Trade_ticker(
            markets=market
        )
        # print_json(resp['result'])
        current_price = resp['result'][0]['trade_price']
        print("##### current price = " + str(current_price))

        if current_price >= (float(buy_price) * (1 + sell_margin_percent/100)):
            sell_price = str(current_price)
            sell_volume = buy_volume

            if program_test:
                print("### sell coin comment out")
                uuid = "cdd92199-2897-4e14-9448-f923320408ad"
            else:
                uuid = sell_coin(client, market, sell_price, sell_volume)
            
            # remove buy file
            os.remove(market_buy_done_file)

            # create sell try file
            market_sell_try_file = market + "_" + file_list[2]
            with open(market_sell_try_file, "w+") as f:

                # save sell price, sell volume, and uuid into sell try file
                f.write(uuid + "," + sell_price + "," + sell_volume + "\n")
                f.close()

            break
        else:
            time.sleep(sleep_sec)
            continue
    
    if x == (loop_count - 1):
        print("#### sell loop count end") 

def buy_status_loop(client, market):

    """ 
    load uuid, price, volume from buy try file
    enter loop to query buy status for uuid
        if buy status is done
            rename buy try file to buy done file
            exit loop
        else
            sleep
            continue loop 
    """

    # file_list = ["buy_try.txt", "buy_done.txt", "sell_try.txt", "sell_done.txt"]
    market_buy_try_file = market + "_" + file_list[0]

    buy_uuid, buy_price, buy_volume = load_price_and_volume(market_buy_try_file)

    for x in range(loop_count):

        if program_test:
            state = "done"
        else:
            resp = client.Order.Order_info(
                # uuid='9ca023a5-851b-4fec-9f0a-48cd83c2eaae'
                uuid=buy_uuid
            )
            print_json(resp['result'])
            state = resp['result']['state']

        if state == "done":
            # rename buy try file to buy done file
            market_buy_done_file = market + "_" + file_list[1]
            os.rename(market_buy_try_file, market_buy_done_file)
            break
        else:
            time.sleep(sleep_sec)
            continue
    
    if x == (loop_count - 1):
        print("#### buy status count end")


def buy_try_loop(client, market, reference_price, buy_margin_percent, buy_krw):

    """     
    if command argument have reference price
        set it to reference price
    else
        query candle price(two week/month, open price, close price, high price, low price)
        compute averaged price, and set it into reference price
    enter loop to query current price
        if current price is 10% less than reference price
            try to buy(bid) coin for price and volume
            keep uuid from order response
            create buy try file
            save buy price, volume, and uuid into buy try file
            exit loop
        else
            sleep
            continue loop 
    """

    for x in range(loop_count):

        # get current price
        # 요청 당시 종목의 스냅샷을 반환합니다.
        resp = client.Trade.Trade_ticker(
            markets=market
        )
        # print_json(resp['result'])
        current_price = resp['result'][0]['trade_price']
        print("##### current price = " + str(current_price))

        if current_price <= (reference_price * (1 + buy_margin_percent/100)):
            buy_volume = "{:.8f}".format(buy_krw / current_price)
            buy_price = str(current_price)
            
            # get uuid from buy order response
            if program_test:
                print("### buy coin comment out")
                uuid = "cdd92199-2897-4e14-9448-f923320408ad"
            else:
                uuid = buy_coin(client, market, buy_price, buy_volume)

            # file_list = ["buy_try.txt", "buy_done.txt", "sell_try.txt", "sell_done.txt"]

            # create buy try file
            market_buy_try_file = market + "_" + file_list[0]
            with open(market_buy_try_file, "w+") as f:
                # save buy price, buy volume, and uuid into buy try file
                f.write(uuid + "," + buy_price + "," + buy_volume + "\n")
                f.close()

            break
        else:
            time.sleep(sleep_sec)
            continue
    
    if x == (loop_count - 1):
        print("#### buy try loop count end")

# pseudo code
""" 
[single trading algorithm: buy coin, and then try to sell it]

get market name from command argument
enter loop to check file exist
    if buy done file exist
        load price and volume from buy done file
        enter loop to query current price
            if current price is 15% more than buy price
                try to sell(ask) coin for price and volume
                keep uuid from order response
                remove buy done file
                create sell try file
                save sell price, volume, and uuid into sell try file
                exit loop
            else
                sleep
                continue loop
    else if buy try file exist
        load price, volume, and uuid from buy try file
        enter loop to query buy status for uuid
            if buy status is done
                rename buy try file to buy done file
                exit loop
            else
                sleep
                continue loop
    else if sell try file exist
        load price, volume, and uuid from sell try file
        enter loop to query sell status for uuid
            if sell status is done
                rename sell try file to sell done file
                prepend timestamp to sell done filename(sell history file)
                exit loop
            else
                sleep
                continue loop
    else (no file exist)
        if command argument have buy price
            set it to initial price
        else
            query candle price(two week/month, open price, close price, high price, low price)
            compute averaged price, and set it into initial price
        enter loop to query current price
            if current price is 10% less than initial price
                try to buy(bid) coin for price and volume
                keep uuid from order response
                create buy try file
                save buy price, volume, and uuid into buy try file
                exit loop
            else
                sleep
                continue loop
"""

if __name__ == "__main__":

    arg_len = len(sys.argv)
    if arg_len == 8:
        user_reference_price = float(sys.argv[7])
        print("##### user reference price = " + str(user_reference_price))
    elif arg_len == 7:
        user_reference_price = 0
    else:
        print("#### command argument error")
        sys.exit()

    market = sys.argv[1]
    average_unit = sys.argv[2]
    unit_count = int(sys.argv[3])
    # this can be negative or positive
    buy_margin_percent = float(sys.argv[4])
    # this must be positive because loss must not be accepted 
    sell_margin_percent = float(sys.argv[5])
    buy_krw = int(sys.argv[6])

    # check market
    if not market in market_list:
        print("#### check market")
        sys.exit()
    else: 
        print("#### market = " + market)

    # check average unit
    if not average_unit in average_unit_list:
        print("### check average unit")
        sys.exit()
    else:
        print("#### average unit = " + average_unit)

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)
    # print(client)

    if not user_reference_price:
        reference_price = get_averaged_price(client, market, average_unit, unit_count)
        print("#### averaged reference price for buy = " + str(reference_price))
    else:
        reference_price = user_reference_price

    user_confirm_message = \
    """ 
    #############################################
    # market = {0}
    # average unit = {1}
    # unit count = {2}
    # reference price = {3}
    # buy margin percent = {4}
    # sell margin percent = {5}
    # buy krw = {6}
    #############################################
    """.format(market, average_unit, unit_count, reference_price, \
        buy_margin_percent, sell_margin_percent, buy_krw)
    print(user_confirm_message)

    user_input = input("confirm trade(yes or no)? ")
    if user_input != "yes":
        print("#### exit trade")
        sys.exit()

    ############ trade file reminder
    # file_list = ["buy_try.txt", "buy_done.txt", "sell_try.txt", "sell_done.txt"]

    while True:

        if exists(market + "_" + file_list[3]):
            timestamp_sell_done(market)

            user_input = input("continue new trade(yes or no)? ")
            if user_input == "yes":
                print("#### continue new trade")
                continue
            else:
                print("#### finish trade")
                sys.exit()
        elif exists(market + "_" + file_list[2]):
            print("### sell status loop enter: " + market)
            sell_status_loop(client, market)
        elif exists(market + "_" + file_list[1]):
            print("### sell try loop enter: " + market)
            sell_try_loop(client, market, sell_margin_percent)  
        elif exists(market + "_" + file_list[0]):
            print("### buy status loop enter: " + market)
            buy_status_loop(client, market)
        else:
            print("### buy try loop enter: " + market)
            buy_try_loop(client, market, reference_price, buy_margin_percent, buy_krw)


""" 
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
    market='KRW-DOGE'
)
print_json(resp['result'])

# 요청 당시 종목의 스냅샷을 반환합니다.
resp = client.Trade.Trade_ticker(
    markets='KRW-DOGE'
)
print_json(resp['result'])
print(resp['result'][0]['trade_price'])

# 주(Week) 단위로 시세 캔들을 조회합니다.
resp = client.Candle.Candle_weeks(
    market='KRW-DOGE',
    count=2
)
print_json(resp['result'])

# 월(Month) 단위로 시세 캔들을 조회합니다.
resp = client.Candle.Candle_month(
    market='KRW-DOGE',
    count=2
)
print_json(resp['result']) 
"""




