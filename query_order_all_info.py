
from doge_trade import *

if __name__ == "__main__":

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    # 주문 리스트를 조회합니다.
    resp = client.Order.Order_info_all()
    print_json(resp['result'])
    