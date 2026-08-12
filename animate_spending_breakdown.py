import streamlit as st
from etl import Expenditure

def select_expenditure(category_name):
    st.session_state.selected_expenditure = category_name
    print("callback called",category_name)

def render_selected(category: Expenditure):
    st.markdown(
        f"""
        <div class="budget-card-selected">
            <div>{category.name}</div>
            <div>{category.percentage:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
    )

def animate_spending_breakdown(categories : list[Expenditure]):

    if "selected_expenditure" not in st.session_state:
        st.session_state.selected_expenditure = None

    selected = st.session_state.selected_expenditure

    widths =[
        max(abs(category.percentage),4)
        for category in categories
    ]

    columns = st.columns(widths, gap=None)

    for column, category in zip(columns,categories):

        with column:

            if selected == category.name:
                render_selected(category)
            else:
                st.button(
                    f"{category.name}\n\n{category.percentage:.1f}%",
                    key=f"category_{category.name}",
                    use_container_width=True,
                    on_click=select_expenditure,
                    args=(category.name,))

