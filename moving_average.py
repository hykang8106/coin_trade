
############################
# (1) "파이썬을 이용한 비트코인 자동매매" 책에 있는 moving average 코드를 구현함
#     https://github.com/sharebook-kr
#
#########################

from doge_trade import *

def moving_average_candle_days(client, market, ma_days):

    # 일(Day) 단위로 시세 캔들을 조회합니다.
    resp = client.Candle.Candle_days(
        market=market,
        # '+1': computing moving average exclude today's trade price
        count=str(ma_days + 1)
    )
    # print_json(resp['result'])

    # get moving average price excluding today's trade price
    ma_price = mean([y['trade_price'] for y in resp['result'][1:]])
    # print(ma_price)

    return ma_price

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("#### give market name(i.e. KRW-ETH), and moving average days")
        print("#### command example: util_book KRW-DOGE 10")
        sys.exit()
    
    market = sys.argv[1]
    ma_days = int(sys.argv[2])

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    ma_price = moving_average_candle_days(client, market, ma_days)
    print(ma_price)



