
from doge_trade import *

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("#### give market name(i.e. KRW-ETH)")
        sys.exit()
    
    market = sys.argv[1]

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    # get current price
    # 요청 당시 종목의 스냅샷을 반환합니다.
    resp = client.Trade.Trade_ticker(
        markets=market
    )
    print_json(resp['result'][0])
