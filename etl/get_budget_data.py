from etl.datamodel import Budget


import pandas as pd
import streamlit as st


@st.cache_data
def get_budget_data()-> Budget:
    dataset_url = "https://www.govinfo.gov/content/pkg/BUDGET-2027-TAB/xls/BUDGET-2027-TAB-2-1.xlsx"
    df = pd.read_excel(dataset_url)
    latest = df.dropna(subset=[df.columns[1]]).iloc[-1]
    return Budget(
        year=int(latest.iloc[0]),
        receipts=int(latest.iloc[1]),
        outlays=int(latest.iloc[2]),
        deficit=int(latest.iloc[3])
    )