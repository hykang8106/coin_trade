
from doge_trade import *

def get_remaining_request():

    client = Upbit(access_key, secret_key)

    resp = client.APIKey.APIKey_info()
    # print_json(resp)

    # get remaining request per minute
    remaining_min = resp["remaining_request"]["min"]
    print("remaining per minute = " + remaining_min)

    # get remaining request per second
    remaining_sec = resp["remaining_request"]["sec"]
    print("remaining per second = " + remaining_sec)

    # get resopnse status code
    status_code = str(resp["response"]["status_code"])
    print("status code = " + status_code)
    # success when status code is 200


def get_remaining_request_in_resp(resp):

    # get remaining request per minute
    remaining_min = resp["remaining_request"]["min"]
    print("remaining per minute = " + remaining_min)

    # get remaining request per second
    remaining_sec = resp["remaining_request"]["sec"]
    print("remaining per second = " + remaining_sec)

    # get resopnse status code
    status_code = str(resp["response"]["status_code"])
    print("status code = " + status_code)
    # success when status code is 200

if __name__ == "__main__":

    if 'resp' in locals():
        print("resp variable exist")
        get_remaining_request_in_resp(resp)
    else:
        get_remaining_request()

    """ remaining_min, remaining_sec, status_code = get_remaining_request_in_resp(resp)

    # remaining request per minute
    print("remaining per minute = " + remaining_min)

    # remaining request per second
    print("remaining per second = " + remaining_sec)

    # resopnse status code
    print("status code = " + str(status_code))
    # success when status code is 200 """
