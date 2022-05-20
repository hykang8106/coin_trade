
############################
# "파이썬을 이용한 비트코인 자동매매" 책에 있는 코드를 구현함
#
# https://github.com/sharebook-kr
#########################

'''
[back test algorithm]


'''

from doge_trade import *

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("#### give market name(i.e. KRW-ETH), and moving average days")
        print("#### command example: back_test KRW-DOGE 10")
        sys.exit()
    
    market = sys.argv[1]
    ma_days = sys.argv[2]

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    # 일(Day) 단위로 시세 캔들을 조회합니다.
    resp = client.Candle.Candle_days(
        market=market,
        count=ma_days
    )
    print_json(resp['result'])

    # get moving average price
    ma_price = mean([y['trade_price'] for y in resp['result']])
    print(ma_price)

    # reference_price = mean([(y['opening_price'] + y['trade_price'])/2 for y in resp['result']])

