
from doge_trade import *

if __name__ == "__main__":

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)
    
    # 전체 계좌 조회
    # 내가 보유한 자산 리스트를 보여줍니다.
    resp = client.Account.Account_info()
    # print(resp['result'])
    print_json(resp['result'])
    