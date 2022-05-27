
import json, sys
import asyncio

from doge_trade import print_json

from upbit.websocket import UpbitWebSocket

valid_service = ["ticker", "trade", "orderbook"]

isOnlySnapshot = False
isOnlyRealtime = True

# Definition async function
async def service(sock, payload):

    async with sock as conn:
        await conn.send(payload)
        while True:
            recv = await conn.recv()
            data = recv.decode('utf8')
            result = json.loads(data)
            print_json(result)
            # print(result)

""" 
async def main(currencies, service_list):
    
    sock = UpbitWebSocket()

    # currencies = ['KRW-BTC', 'KRW-ETH']
    # currencies = market_list
    counts = [1 for _ in range(len(currencies))]

    ord_codes = sock.generate_orderbook_codes(
        currencies=currencies,
        counts=counts
    )

    orderbook = sock.generate_type_field(
        # 현재가: 'ticker', 체결: trade, 호가: orderbook
        type='orderbook',
        codes=ord_codes
    )

    ticker = sock.generate_type_field(
        # 현재가: 'ticker', 체결: trade, 호가: orderbook
        type='ticker',
        codes=currencies
        # 시세 스냅샷만 제공, 생략 가능
        # isOnlySnapshot = True
        # 실시간 시세만 제공, 생략 가능
        # isOnlyRealtime = True
    )

    trade = sock.generate_type_field(
        # 현재가: 'ticker', 체결: trade, 호가: orderbook
        type='trade',
        codes=currencies
        # 시세 스냅샷만 제공, 생략 가능
        # isOnlySnapshot = True
        # 실시간 시세만 제공, 생략 가능
        # isOnlyRealtime = True
    )

    payload = sock.generate_payload(
        type_fields=[ticker, trade, orderbook]
    )

    print(payload)

    await service(sock, payload) 
"""

async def new_main(currencies, service_list):
    
    sock = UpbitWebSocket()

    type_fields = []

    for s in service_list:

        if s == "orderbook":

            # currencies = ['KRW-BTC', 'KRW-ETH']
            # currencies = market_list
            counts = [1 for _ in range(len(currencies))]

            ord_codes = sock.generate_orderbook_codes(
                currencies=currencies,
                counts=counts
            )

            orderbook = sock.generate_type_field(
                # 현재가: 'ticker', 체결: 'trade', 호가: 'orderbook'
                type='orderbook',
                codes=ord_codes,
                # 시세 스냅샷만 제공, 생략 가능
                isOnlySnapshot = isOnlySnapshot,
                # 실시간 시세만 제공, 생략 가능
                isOnlyRealtime = isOnlyRealtime
            )

            type_fields.append(orderbook)

        if s == "ticker":

            ticker = sock.generate_type_field(
                # 현재가: 'ticker', 체결: 'trade', 호가: 'orderbook'
                type='ticker',
                codes=currencies,
                # 시세 스냅샷만 제공, 생략 가능
                isOnlySnapshot = isOnlySnapshot,
                # 실시간 시세만 제공, 생략 가능
                isOnlyRealtime = isOnlyRealtime
            )

            type_fields.append(ticker)

        if s == "trade":

            trade = sock.generate_type_field(
                # 현재가: 'ticker', 체결: 'trade', 호가: 'orderbook'
                type='trade',
                codes=currencies,
                # 시세 스냅샷만 제공, 생략 가능
                isOnlySnapshot = isOnlySnapshot,
                # 실시간 시세만 제공, 생략 가능
                isOnlyRealtime = isOnlyRealtime
            )

            type_fields.append(trade)

    # print(type_fields)
    
    payload = sock.generate_payload(
        type_fields=type_fields
    )

    # print(payload)

    await service(sock, payload)

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("### must give market, [service type]")
        #### service type not allow space: [ticker,trade,odrderbook] 
        print("### example: websocket_service KRW-ETH [ticker,trade,odrderbook]")
        sys.exit()

    market_list = []
    market_list.append(sys.argv[1])
    #############################
    # first code was:
    # market_list = list(map(str, sys.argv[1].strip('[]').split(',')))
    #
    # websocket_example [kRW-ETH,KRW-BTC] [ticker,trade,odrderbook]
    #
    # in ipython, above not working
    # in python, above working
    # but in ipython, [kRWETH,KRWBTC] working, 
    # why? "-" character give error?
    #
    # so use only one market in ipython
    #############################

    service_list = list(map(str, sys.argv[2].strip('[]').split(',')))
    print(market_list, service_list)

    for n in service_list:
        if not n in valid_service:
            print("#### '{}' is invalid service".format(n))
            sys.exit()
    
    #### "new_main" working, use it instead of "main"
    asyncio.run(new_main(market_list, service_list))


""" 
codes = ['KRW-BTC', 'KRW-ETH', 'KRW-BCH', 'KRW-XRP']
counts = [1 for _ in range(len(codes))]

ord_codes = UpbitWebSocket.generate_orderbook_codes(
    currencies=codes,
    counts=counts
)

orderbook = UpbitWebSocket.generate_type_field(
    type='orderbook',
    codes=ord_codes
)

trade = UpbitWebSocket.generate_type_field(
    type='trade',
    codes=codes
)

ticker = UpbitWebSocket.generate_type_field(
    type='ticker',
    codes=codes
)

type_fields = [trade, orderbook, ticker]

payload = UpbitWebSocket.generate_payload(
    type_fields=type_fields,
    format='SIMPLE'
)

print(payload) 
"""


""" 
sock = UpbitWebSocket()

currencies = ['KRW-BTC', 'KRW-ETH']
type_field = sock.generate_type_field(
    type='ticker',
    codes=currencies
)
payload = sock.generate_payload(
    type_fields=[type_field]
)

#### below give error
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete( ticker(sock, payload) ) 
"""