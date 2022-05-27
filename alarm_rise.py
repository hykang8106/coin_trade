
###### test result: 
#
# ConnectionError: 
# ('Connection aborted.', ConnectionResetError(10054, 
# '현재 연결은 원격 호스트에 의해 강제로 끊겼습니다', None, 10054, None)) 
#
# my suspect: remaining request per minute is exhausted?
#############

"""   
    "remaining_request": {
      "group": "candles",
      "min": "599",
      "sec": "9"
    },
    "response": {
      "url": "https://api.upbit.com/v1/candles/days?market=KRW-DOGE&to=2021-09-30+09%3A00%3A00&count=200",
      "headers": "{'Date': 'Sat, 21 May 2022 13:57:58 GMT', 'Content-Type': 'application/json;charset=UTF-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Remaining-Req': 'group=candles; min=599; sec=9', 'Vary': 'origin,access-control-request-method,access-control-request-headers,accept-encoding', 'X-Frame-Options': 'DENY', 'Expires': '0', 'ETag': 'W/\"09763e0fcb1acec6cbaa60b8efe8df62f\"', 'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '1; mode=block', 'Cache-Control': 'no-cache, no-store, max-age=0, must-revalidate', 'Pragma': 'no-cache', 'Content-Encoding': 'gzip'}",
      "status_code": 200,
      "reason": "",
      "text": "[{\"market\":\"KRW-DOGE\",\"candle_date_time_utc\"...
    "result": {...
"""

###########################
# for remaining request code, see "get_remaining_request.py"
###########################

from doge_trade import *

loop_limit = 2**20

# back_test_sleep_sec = 60

'''
set rise counter to 0
enter loop to get market snapshot
    get trade price
    save it to current trade price
    if loop count is 1
        get prev closing price
        save it to previous trade price
    compute difference of trade price(difference = current - previous)
    if difference is positive
        increment rise counter
        if rise counter == buy number
            break
    else
        set rise counter to 0
    save current signed change price to previous signed change price
    sleep
sleep
get market snapshot
get trade price
save it to current trade price
compute difference of trade price(difference = current - previous)
if difference is positive
    return pass
else 
    return fail
'''

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("#### give market name(i.e. KRW-ETH), consecutive rise number, and interval sec")
        print("#### command example: alarm_rise KRW-DOGE 5 10")
        sys.exit()
    
    market = sys.argv[1]
    buy_number = int(sys.argv[2])
    sleep_sec = int(sys.argv[3])

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    # print("buy number = " + str(buy_number))
    rise_counter = 0

    for x in range(loop_limit):

        # get current price
        # 요청 당시 종목의 스냅샷을 반환합니다.
        resp = client.Trade.Trade_ticker(
            markets=market
        )
        # print_json(resp['result'][0])

        current = resp['result'][0]['trade_price']
        if x == 0:
            prev_closing_price = resp['result'][0]['prev_closing_price']
            previous = prev_closing_price
        if (current - previous) > 0:
            rise_counter += 1
            if rise_counter == buy_number:
                rise_counter = 0
                print("######## reach buy number")
        else:
            rise_counter = 0
        
        previous = current
        print("trade price = {}, signed change price = {}".\
            format(resp['result'][0]['trade_price'], resp['result'][0]['signed_change_price']))

        """ print(resp['result'][0]['trade_price'])
        print(resp['result'][0]['signed_change_price']) """

        time.sleep(sleep_sec)  





    
