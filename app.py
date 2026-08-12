
#%%
import streamlit as st
from etl import get_budget_data,get_major_categories,get_expenditure_by_function
from show_budget_intro import show_budget_intro
from animate_initial_spending import animate_initial_spending
from etl import load_css_for_streamlit_controls

def start_budget():
    st.session_state.started=True

load_css_for_streamlit_controls("style.css")

budget = get_budget_data()
st.title(f"The USA: A Household Budget - {budget.year}")
intro = st.empty()

if "started" not in st.session_state:
    st.session_state.started = False

if "selected_expenditure" not in st.session_state:
    st.session_state.selected_expenditure = None

tax_receipts = budget.receipts/1_000_000
spent = budget.outlays/1_000_000
gap = abs(budget.deficit)/1_000_000


if not st.session_state.started:
    show_budget_intro(
        intro,
        tax_receipts,
        spent,
        gap
    )
    st.button("Start ->",on_click=start_budget)

if st.session_state.started:
    st.subheader("Here's how that breaks down")

    expenditures = get_expenditure_by_function(budget.outlays)
    categories = get_major_categories(expenditures)

    should_animate = not st.session_state.get(
        "initial_spending_done",
        False
    )

    result = animate_initial_spending(
        total_spending=spent,
        categories=categories,
        animate=should_animate
    )

    if should_animate:
        st.session_state.initial_spending_done = True

    selected_gao_code = None
    selected_gao_category =None
    selected_gao_description = None

    if result.selected is not None:
        st.session_state.selected_expenditure = result.selected
        selected_gao_code = result.selected["gao_code"]
        selected_gao_category = result.selected["category"]
        selected_gao_description = next(
            (
                category.gao_function.description
                for category in categories
                if category.gao_function
                and category.gao_function.code == selected_gao_code
            ),
            None
        )

    st.markdown(
                        """
                        <small><i>
                        Data Source: GovInfo.gov —
                        <a href="https://www.govinfo.gov/app/details/BUDGET-2027-TAB/BUDGET-2027-TAB-4-1">
                        GovInfo.Gov: Budget FY 2027 - Table 3.1 - Outlays by Superfunction and Function: 1940-2031
                        </a>
                        </i></small>
                        """,
                        unsafe_allow_html=True
                    )
    st.markdown(
                            """
                            <small><i>
                            Taxonomy Source: Gao.Gov —
                            <a href="https://www.gao.gov/assets/a76916.html">
                            GAO-05-734SP : 'A Glossary of Terms Used in the Federal Budget Process
                            </a>
                            </i></small>
                            """,
                            unsafe_allow_html=True
                        )
    st.write("Selected expenditure:", selected_gao_category if selected_gao_category else '')
    if selected_gao_description:
        st.write(selected_gao_description)
    

# %%
