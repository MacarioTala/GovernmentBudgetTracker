import pandas as pd
from etl.datamodel import TreasuryYieldCurve
from datetime import date
import streamlit as st

@st.cache_data
def get_treasury_yeild(date_string: str |None=None):
    """
    Gets the latest US Treasury Yield.
    Usage: get_treasury_yeild(date_string) where date_string is of the format: YYYYMM
    If you pass nothing, you get yields as of today
    eg:
        get_treasury_yeild("202608")
        will get the yeild as of August 2026
    """
    if date_string is None:
        date_string = date.today().strftime("%Y%m")
    treasury_yield_url =f"https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/all/{date_string}?type=daily_treasury_yield_curve&field_tdr_date_value_month={date_string}&page&_format=csv"
    df=pd.read_csv(treasury_yield_url)
    df["Date"]=pd.to_datetime(df["Date"])

    latest = df.loc[df["Date"].idxmax()]

    return TreasuryYieldCurve(
        date=latest["Date"].date(),
        one_month=latest["1 Mo"],
        one_point_five_month=latest["1.5 Month"],
        two_month=latest["2 Mo"],
        three_month=latest["3 Mo"],
        four_month=latest["4 Mo"],
        six_month=latest["6 Mo"],
        one_year=latest["1 Yr"],
        two_year=latest["2 Yr"],
        three_year=latest["3 Yr"],
        five_year=latest["5 Yr"],
        seven_year=latest["7 Yr"],
        ten_year=latest["10 Yr"],
        twenty_year=latest["20 Yr"],
        thirty_year=latest["30 Yr"]
    )