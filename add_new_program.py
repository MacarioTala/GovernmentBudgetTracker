import streamlit as st
from etl.datamodel import GAOFunction,Expenditure,ExpenditureDisplay

@st.dialog("New Program")
def add_new_program(current_total_spending:int):
    with st.form("new_program_form"):
        if "new_programs" not in st.session_state:
            st.session_state.new_programs = []

        name = st.text_input(
            "Program name",
            placeholder="Give your new program a title"
        )

        description = st.text_area(
            "Description",
            placeholder="... and a description"
        )

        amount = st.number_input(
            "Annual Cost in millions",
            min_value=0,
            format="%d"
        )

        gao_code = st.text_input(
            "GAO Function Code",
            value="800",
             help="Code 800 is the code for ‘General Government’. Leave this as is unless you feel strongly about rolling your program up into another government function."
        )

        submit_column,cancelled_column = st.columns([1,1])

        with submit_column:
            submitted = st.form_submit_button(
                "Add Program",
                type="primary"
            )

        with cancelled_column:
            cancelled = st.form_submit_button("Cancel")

        if cancelled:
            st.rerun()

        if submitted:
            gao_function = GAOFunction(
                code=gao_code,
                name=name,
                description=description
            )

            expenditure = Expenditure(
                name=name,
                amount=amount,
                percentage=(amount/current_total_spending)*100,
                level=1,
                gao_function=gao_function
            )

            st.session_state.new_programs.append(
                ExpenditureDisplay(expenditure=expenditure)
                )
            st.rerun()