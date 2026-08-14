import streamlit as st
from convenience import human_conceivable_number
from animate_bar.animate_bar import animate_bar

def rough_budget_balancing(spent: int, tax_receipts: int,gap: int):
    st.header("Here's that budget bar again")
    animate_bar(
                        "Spending:",
                        amount=spent,
                        max_amount=spent,
                        threshold=tax_receipts)
    st.subheader(f"You need ${human_conceivable_number(gap*1000000)}")

    btn_cut_spending,btn_borrow,buffer = st.columns([1.2,1.2,6])

    with btn_cut_spending:
        st.button("Cut spending")

    with btn_borrow:
        st.button("Increase deficit")
    