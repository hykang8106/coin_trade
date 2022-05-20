
from doge_trade import *

if __name__ == "__main__":

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)
    
    # 내가 보유한 자산 리스트를 보여줍니다.
    resp = client.Deposit.Deposit_coin_addresses()
    print_json(resp['result'])
