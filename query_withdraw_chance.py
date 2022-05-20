
from doge_trade import *

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("#### give currency name(i.e. ETH, DOGE, ADA)")
        sys.exit()
    
    currency = sys.argv[1]

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    # 출금 리스트 조회합니다.
    #########################################
    # 출금 코인 주소가 등록되어 있지않으므로, return 값이 empty([]).
    #########################################
    resp = client.Withdraw.Withdraw_info_all()
    print_json(resp['result'])

    # 해당 통화의 가능한 출금 정보를 확인합니다.
    resp = client.Withdraw.Withdraw_chance(
        currency=currency
    )
    print_json(resp['result'])