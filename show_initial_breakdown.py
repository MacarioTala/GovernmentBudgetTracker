from animate_initial_spending import animate_initial_spending
from convenience import gao_lookup, human_conceivable_number
from etl.datamodel import ExpenditureDisplay
import streamlit as st


def show_initial_breakdown(budget, spent, expense_categories : list[ExpenditureDisplay], gao_functions):
    result = animate_initial_spending(
        total_spending=spent,
        categories=expense_categories
    )

    selected_gao_code = None
    selected_gao_description = None
    expenditure_amount = None
    selected_gao = None

    if result.selected is not None:
        st.session_state.selected_expenditure = result.selected
        selected_gao_code = result.selected["gao_code"]

        selected_gao = next(
                expense_category
                for expense_category in expense_categories
                if expense_category.expenditure.gao_function
                and expense_category.expenditure.gao_function.code == selected_gao_code
            )
        selected_gao_description = selected_gao.expenditure.gao_function.description
        expenditure_amount = selected_gao.expenditure.amount
        

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
        tldr=None
        if expenditure_amount>0:
            tldr = f"**This cost USD${human_conceivable_number(expenditure_amount)} in {budget.year}**"
        else:
            tldr = f"**This saved USD${human_conceivable_number(expenditure_amount)} in {budget.year}**" 
        st.header(tldr)

    if selected_gao_description:
        st.write(selected_gao_description)

    if selected_gao and selected_gao.expenditure.gao_function.subcodes:
        st.subheader("*This has the following subfunctions*")
        for subcode in selected_gao.expenditure.gao_function.subcodes:
            expenditure_to_display = gao_lookup(gao_functions,subcode)
            st.write(f"**{subcode} {expenditure_to_display.name}**")
            st.write(expenditure_to_display.description)

    if selected_gao and selected_gao.children:
        st.subheader("This expense rolls up the following expenses")
        rows = [
                {
                    "GAO Code": child.gao_function.code,
                    "Function": child.gao_function.name,
                    "Amount" : f"USD$ {human_conceivable_number(child.amount)}",
                    "Percentage": f"{child.percentage:.2f}"
                }
                for child in selected_gao.children
            ]
        rows.append(
            {
                "GAO Code": "",
                "Function": "Total",
                "Amount": f"${human_conceivable_number(sum(x.amount for x in selected_gao.children))}",
                "Percentage": f"{sum(x.percentage for x in selected_gao.children):.2f}%"
})
        st.table(rows)
