###########
# back test file version:
#
# (1) get candle days for back test from excel file
###############

############################
# "파이썬을 이용한 비트코인 자동매매" 책에 있는 코드를 구현함, ch 7
#
# https://github.com/sharebook-kr
#########################

""" 
[ref] https://blockworks.co/crypto-is-more-correlated-with-tech-stocks-than-ever-how-do-we-decouple/

Indeed, crypto and equity markets are increasingly correlated, 
particularly with tech stocks, as bitcoin’s price has tracked blue chip tech stocks 
such as Apple, Amazon and Microsoft all year.

And little has changed in the most recent downturn. 
In fact, correlation is tightening.  
"""

'''
[back test algorithm]


'''

import numpy as np
import pandas as pd

from doge_trade import *
# from get_remaining_request import *

fee = 0.001

# get_optimal_k = True

def get_candle_df_from_file(filename, from_date_str, to_date_str):

    candle_df = pd.read_excel(filename, engine="openpyxl")

    #######################
    # code here to get candle data only met with condition from_date_str, to_date_str
    ##################

    return candle_df

def back_test(df, k=0.5):

    # moving average days, 5 is optimal to check 'bull' market?
    ma_days = 5

    df['ma'] = df['trade_price'].rolling(window=ma_days).mean().shift(1)
    df['range'] = (df['high_price'] - df['low_price']) * k
    df['target'] = df['opening_price'] + df['range'].shift(1)
    df['bull'] = df['opening_price'] > df['ma']

    # ror = rate of return
    df['ror'] = np.where((df['high_price'] > df['target']) & df['bull'], \
                    df['trade_price'] / df['target'] - fee, 1)

    # hpr = holding period return
    # when "back_test KRW-DOGE day 2021-09-30 200", last hpr is computed for last 200 days to 2021-09-30 
    df['hpr'] = df['ror'].cumprod()

    # dd: draw down
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    
    return df


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("#### give filename, market name(i.e. KRW-ETH), from date, to date")
        print("#### example: back_test_file KRW-DOGE_2021-02-24_2022-05-23.xlsx KRW-DOGE 2021-09-30 2022-05-23")
        sys.exit()
    
    filename = sys.argv[1]
    market = sys.argv[2]
    from_date_str = sys.argv[3]
    to_date_str = sys.argv[4]

    if not exists(filename):
        print("### file not found")
        sys.exit()

    filebase, _ = os.path.splitext(filename)
    f_market, f_from_date, f_to_date = filebase.split("_")
    if f_market != market:
        print("### market name not in filename")
        sys.exit()

    if f_from_date > from_date_str:
        from_date_str = f_from_date

    if f_to_date < to_date_str:
        to_date_str = f_to_date

    print("back test = {} ~ {}".format(from_date_str, to_date_str))
    candle_df = get_candle_df_from_file(filename, from_date_str, to_date_str)

    # default k = 0.5 is used
    candle_df = back_test(candle_df)

    # hpr = holding period return
    # when "back_test KRW-DOGE day 2021-09-30 200", last hpr is computed for last 200 days to 2021-09-30
    # why -2, not -1?
    last_hpr = candle_df['hpr'].iloc[-2]
    print("last hpr = ", last_hpr)
    
    # max draw down
    max_dd = candle_df['dd'].max()
    print("MDD(%): ", max_dd)

    """ if get_optimal_k:

        candle_df = get_candle_df(client, market, last_candle_date, candle_num)

        # get optimal k which is used to compute price range, 
        # df['range'] = (df['high_price'] - df['low_price']) * k
        last_hpr_list = list()
        k_list = np.arange(0.1, 1.1, 0.1)
        for k in k_list:
            candle_df = back_test(candle_df, k)
            last_hpr = candle_df['hpr'].iloc[-2]
            last_hpr_list.append(last_hpr)
            print("k = {:.1f}, last hpr = {:f}".format(k, last_hpr))

        print(last_hpr_list)
        max_last_hpr = max(last_hpr_list)
        max_index = last_hpr_list.index(max_last_hpr)
        print("when k = {:.1f}, max last hpr = {:f}".format(k_list[max_index], max_last_hpr)) """
    
