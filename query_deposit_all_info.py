
from doge_trade import *

if __name__ == "__main__":

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    # 입금 리스트 조회합니다.
    resp = client.Deposit.Deposit_info_all()
    print_json(resp['result'])