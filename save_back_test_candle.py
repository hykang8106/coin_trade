
from datetime import date, timedelta
import pandas as pd

from doge_trade import *
from get_remaining_request import *

max_candle_days = 200

filename = "back_test_candle.xlsx"

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("#### give market name(i.e. KRW-ETH), from date, to date")
        print("#### command example: save_back_test_candle KRW-DOGE 2021-09-30 2022-05-21")
        sys.exit()

    market = sys.argv[1]
    from_date_str = sys.argv[2]
    to_date_str = sys.argv[3]

    from_year, from_month, from_day = from_date_str.split("-")
    to_year, to_month, to_day = to_date_str.split("-")
    from_date = date(int(from_year), int(from_month), int(from_day))
    to_date = date(int(to_year), int(to_month), int(to_day))
    delta = to_date - from_date
        
    # '+1' include "to_date"
    delta_days = delta.days + 1
    print("delta_days = ", delta_days)

    day_point = list(range(0, delta_days, max_candle_days))
    day_point.append(delta_days)
    print("day point = ", day_point)

    # [ref] https://stackoverflow.com/questions/5314241/difference-between-consecutive-elements-in-list
    candle_num = [t - s for s, t in zip(day_point, day_point[1:])]
    print("candle number = ", candle_num)

    # 클라이언트 객체 생성
    client = Upbit(access_key, secret_key)

    candle_df = pd.DataFrame()
    candle_date = to_date
    for n in range(len(candle_num)):
        # print(n)
        print("##### [{}] candle date = {}, candle number = {}".\
            format(n, str(candle_date), candle_num[n]))
        # print(candle_num[n])

        # 일(Day) 단위로 시세 캔들을 조회합니다.
        resp = client.Candle.Candle_days(
            market=market,
            to=str(candle_date) + " 09:00:00",
            count=candle_num[n]
        )
        # print_json(resp['result'])

        df = pd.DataFrame(resp['result'])
        # "KRW-DOGE" candle begin from "2021-02-24"
        if df.empty:
            print("#### empty candle")
            break

        print(df)
        candle_df = pd.concat([candle_df, df], ignore_index=True)

        candle_date = candle_date - timedelta(candle_num[n])

        get_remaining_request_in_resp(resp)

        time.sleep(10)
    
    candle_df = candle_df.sort_values(by=['candle_date_time_utc']).reset_index(drop=True)
    print(candle_df)

    # update "from_date_str" with first row of dataframe
    # because "from_date_str" in command argument may not be satisfied(no candle)
    from_date_str = candle_df['candle_date_time_utc'].iloc[0].split("T")[0]

    filename = "{}_{}_{}.xlsx".format(market, from_date_str, to_date_str)
    candle_df.to_excel(filename, index=False)

    # my pandas version is 1.1.0, in which default engine is "none"
    # but in version 1.3.0, default engine is "openpyxl"
    # so upgrade pandas version?
    candle_df = pd.read_excel(filename, engine="openpyxl")
    print(candle_df)

    