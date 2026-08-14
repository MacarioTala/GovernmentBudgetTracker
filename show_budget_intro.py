import streamlit as st
from animate_bar.animate_bar import animate_bar

def show_budget_intro(
          intro,
          tax_receipts,
          spent,
          gap):
    with intro.container():
            st.header("Here's what we took in and spent last year")
            animate_bar(
                "Income:",
                amount=tax_receipts,
                max_amount=spent)

            animate_bar(
                "Spending:",
                amount=spent,
                max_amount=spent,
                threshold=tax_receipts)

            income,spending =st.columns(2)
            with income:
                st.metric(
                    "Income",
                    f"${tax_receipts:.2f} trillion"
                )

            with spending:
                st.metric(
                    "Spent",
                    f"${spent:.2f} trillion"
                )

            st.metric(
                "Budget gap",
                f"${gap:.2f} trillion")

            st.markdown(
                """
                <small><i>
                Source: GovInfo.gov —
                <a href="https://www.govinfo.gov/app/details/BUDGET-2027-TAB/BUDGET-2027-TAB-2-1">
                Table 1.1 - Summary of Receipts, Outlays, and Surpluses or Deficits (-): 1789-2025
                </a>
                </i></small>
                """,
                unsafe_allow_html=True
            )

            st.write(f"If we changed absolutely nothing and didn't grow, we would need to borrow another {gap:.2f} trillion, adjusted for inflation.")
            st.write("Think you can balance the budget?")