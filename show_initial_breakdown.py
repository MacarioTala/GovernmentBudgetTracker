from animate_initial_spending import animate_initial_spending
from convenience import gao_lookup, human_conceivable_number


import streamlit as st


def show_initial_breakdown(budget, spent, expenditures, categories, gao_functions):
    result = animate_initial_spending(
        total_spending=spent,
        categories=categories
    )

    selected_gao_code = None
    selected_gao_description = None
    expenditure_amount = None
    selected_gao = None

    if result.selected is not None:
        st.session_state.selected_expenditure = result.selected
        selected_gao_code = result.selected["gao_code"]
        selected_gao = next(
            (
                category.gao_function
                for category in categories
                if category.gao_function
                and category.gao_function.code == selected_gao_code
            ),
            None
        )
        selected_gao_description = selected_gao.description
        expenditure_amount = next(
            expenditure.amount
            for expenditure in expenditures
            if expenditure.gao_function
            and expenditure.gao_function.code == selected_gao_code
        )

    st.markdown(
                        """
                        <small><i>
                        Data Source: GovInfo
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
                            Taxonomy Source: US Government Accountability Office
                            <a href="https://www.gao.gov/assets/a76916.html">
                            GAO-05-734SP : A Glossary of Terms Used in the Federal Budget Process
                            </a>
                            </i></small>
                            """,
                            unsafe_allow_html=True
                        )
    st.write("Click each function to see more details")
    st.write("When you're ready, click next, and let's balance the budget!")
    if expenditure_amount:
        st.header(f"**This cost USD${human_conceivable_number(expenditure_amount)} in {budget.year}**")

    if selected_gao_description:
        st.write(selected_gao_description)

    if selected_gao and selected_gao.subcodes:
        st.subheader("*This has the following subfunctions*")
        for subcode in selected_gao.subcodes:
            expenditure_to_display = gao_lookup(gao_functions,subcode)
            st.write(f"**{subcode} {expenditure_to_display.name}**")
            st.write(expenditure_to_display.description)