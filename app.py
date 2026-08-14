
#%%
import streamlit as st
from etl import get_budget_data,get_major_categories,get_expenditure_by_function
from show_budget_intro import show_budget_intro
from rough_budget_balancing import rough_budget_balancing
from etl import load_css_for_streamlit_controls,get_GAO_functions
from show_initial_breakdown import show_initial_breakdown

st.set_page_config(page_title="The USA: A Household Budget")
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

st.title(f"The USA: A Household Budget - {budget.year}")
intro = st.empty()

tax_receipts = budget.receipts/1_000_000
spent = budget.outlays/1_000_000
gap = abs(budget.deficit)/1_000_000

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

    #etl section - cached in module
    expenditures = get_expenditure_by_function(budget.outlays)
    categories = get_major_categories(expenditures)
    gao_functions = get_GAO_functions()

    show_initial_breakdown(budget, spent, expenditures, categories, gao_functions)

elif st.session_state.stage == "rough_balance":
    rough_budget_balancing(spent,tax_receipts,gap)

# %%
