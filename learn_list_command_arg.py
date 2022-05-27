
# [ref] https://stackoverflow.com/questions/4071396/split-by-comma-and-strip-whitespace-in-python

import sys

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("### must give market, service type")
        print("### example: websocket_example kRW-ETH [ticker,trade,odrderbook]")
        sys.exit()

    print(sys.argv[1])
    market_list = list(map(str, sys.argv[1].strip('[]').split(',')))
    service_list = list(map(str, sys.argv[2].strip('[]').split(',')))
    print(market_list, service_list)
    sys.exit()