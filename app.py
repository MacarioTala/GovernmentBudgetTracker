
#%%
import streamlit as st
from etl.etl_convenience import load_css_for_streamlit_controls
from etl.get_GAO_functions import get_GAO_functions
from etl.get_budget_data import get_budget_data
from etl.get_expenditure_by_function import get_expenditure_by_function
from etl.get_major_categories import get_major_categories
from etl.get_treasury_yield import get_treasury_yield
from show_budget_intro import show_budget_intro
from rough_budget_balancing import rough_budget_balancing
from show_initial_breakdown import show_initial_breakdown

st.set_page_config(page_title="Balance The Budget")
if "stage" not in st.session_state:
    st.session_state.stage = "intro"

if "selected_expenditure" not in st.session_state:
    st.session_state.selected_expenditure = None

def transition_to_breakdown():
    st.session_state.stage = "initial_breakdown"

def start_rough_balance():
    st.session_state.stage="rough_balance"

load_css_for_streamlit_controls("style.css")

budget = get_budget_data()

st.title(f"Balance The Budget - {budget.year}")
intro = st.empty()

tax_receipts = budget.receipts
spent = budget.outlays
gap = max(0,spent-tax_receipts)
 #etl section - cached in module
current_yields = get_treasury_yield()
one_year_yield = current_yields.one_year
thirty_year_yield = current_yields.thirty_year
threshold_for_major_category_inclusion = 10
expenditures = get_expenditure_by_function(budget.outlays)
expenditure_displays = get_major_categories(expenditures,threshold_for_major_category_inclusion)
gao_functions = get_GAO_functions()

if st.session_state.stage=="intro":
    show_budget_intro(
        intro,
        tax_receipts,
        spent,
        gap
    )
    st.button("Start ->",on_click=transition_to_breakdown)

elif st.session_state.stage == "initial_breakdown":
    title_column,next_column = st.columns([.87,.13])

    with title_column:
        st.subheader("Here's how that breaks down")

    with next_column:
        st.button("Next->", use_container_width=True,on_click=start_rough_balance)

    show_initial_breakdown(budget, spent, expenditure_displays, gao_functions)

elif st.session_state.stage == "rough_balance":
    rough_budget_balancing(tax_receipts,expenditure_displays,one_year_yield,thirty_year_yield)

# %%
