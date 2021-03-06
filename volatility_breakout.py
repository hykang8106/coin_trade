
##################################################
# "파이썬을 이용한 비트코인 자동매매" 책, ch 6.2
# 
# volatility breakout strategy in 
# "long-term secrets to short-term trading" book by larry williams
#
# (1) 가격 변동폭 계산: 전일 고가에서 전일 저가를 빼서 가격변동폭을 구함
# (2) 매수 기준: 당일 시간에서 (변동폭 * 0.5) 이상 상승하면 해당 가격에 바로 매수
# (3) 매도 기준: 당일 종가에 매도
#############################################

from doge_trade import *

# "import datetime" is not needed
# because "doge_trade.py" have "from datetime import datetime"
# only need import "timedelta"
from datetime import timedelta

def get_buy_target_price(client, market):

    # 일(Day) 단위로 시세 캔들을 조회합니다.
    resp = client.Candle.Candle_days(
        market=market,
        # '2': yesterday and today
        count='2'
    )
    # print_json(resp['result'])

    today = resp['result'][0]
    yesterday = resp['result'][1]

    return today['opening_price'] + (yesterday['high_price'] - yesterday['low_price']) * 0.5

def get_current_price(client, market):


    return current_price

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("#### give market name(i.e. KRW-ETH)")
        print("#### command example: volatility_breakout KRW-DOGE")
        sys.exit()
    
    market = sys.argv[1]

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    now = datetime.now()
    kst09am = datetime(now.year, now.month, now.day) + timedelta(hours=9)

    buy_target_price = get_buy_target_price(client, market)
    print(buy_target_price)

    while True:

        now = datetime.now()
        if kst09am < now < kst09am + timedelta(seconds=10) : 
            buy_target_price = get_buy_target_price(client, market)
            print(buy_target_price)
            kst09am = datetime(now.year, now.month, now.day) + timedelta(hours=9)

            print("###### sell")

        """ current_price = get_current_price(client, market)
        if current_price > buy_target_price:
            print("####### buy") """

        time.sleep(1)

    

