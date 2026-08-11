
#%%
import streamlit as st
from etl import get_budget_data,get_major_categories,get_expenditure_by_function
from animate_bar import animate_bar
from animate_spending_breakdown import animate_spending_breakdown

def load_css(filename):
    with open(filename) as f:
        st.html(f"<style>{f.read()}</style>")

load_css("style.css")
budget = get_budget_data()

if "started" not in st.session_state:
    st.session_state.started = False

st.title(f"The USA: A Household Budget - {budget.year}")

tax_receipts = budget.receipts/1_000_000
spent = budget.outlays/1_000_000
gap = abs(budget.deficit)/1_000_000

total_budget = spent

income_pct=(tax_receipts/total_budget)*100
gap_pct=(gap/total_budget)*100

def start_budget():
    st.session_state.started=True

if not st.session_state.started:
    st.write("Here's what we took in and spent last year")
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

    st.write(f"If we changed absolutely nothing and didn't grow, we would need to borrow another {gap:.2f} trillion")
    st.write("Think you can balance the budget?")

    st.button("Start ->",on_click=start_budget)

if st.session_state.started:
    st.subheader("Here's how that breaks down")

    expenditures = get_expenditure_by_function(budget.outlays)
    categories = get_major_categories(expenditures)

    animate_spending_breakdown(
        total_spending=budget.outlays / 1_000_000,
        categories=categories
    )

# %%
