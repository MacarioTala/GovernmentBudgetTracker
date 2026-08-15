import streamlit as st
from convenience import human_conceivable_number
from etl.datamodel import ExpenditureDisplay
from budget_balancing.render_balance_bar import render_balance_bar

def rough_budget_balancing(spent: int, tax_receipts: int,gap: int, expenditure_displays : list[ExpenditureDisplay]):

    total_cuts=0
    tax_receipts=tax_receipts*1_000_000
    gap=gap*1_000_000
    remaining_gap=gap
    total_spending=spent*1_000_000

    yn_column,btn_finalize_column = st.columns([.87,.13])
    with yn_column:
        you_need_header=st.empty()

    with btn_finalize_column:
         st.button("Finalize Budget->")

    balance_bar = st.empty()

    borrow_label_column,borrow_text_box,borrow_slider_column=st.columns([1,1,2])
    with borrow_label_column:
        st.write("Borrow money")

    with borrow_slider_column:
        borrow_percentage=st.slider(
            "Borrow",
            min_value=0,
            max_value=100,
            value=0,
            label_visibility="collapsed",
            key="borrow_percentage",
            step=1
        )
        borrow_amount = int(gap*(borrow_percentage/100))

    with borrow_text_box:
            st.write(f"**${human_conceivable_number(borrow_amount)}**")

    for display in expenditure_displays:
        if display.expenditure.amount <=0: continue
        label_column,slider_column = st.columns([1,2])

        with slider_column:
            cut_percentage=st.slider(
                "Cut",
                min_value=0,
                max_value=100,
                value=0,
                key=f"cut_{display.expenditure.gao_function.code}",
                label_visibility="collapsed"
                      )
            cut_amount=int(
                (display.expenditure.amount)
                *(cut_percentage/100))
            total_cuts+=cut_amount
            
        with label_column:
                    st.write(f"{display.expenditure.name}")
                    st.caption(f"${human_conceivable_number(display.expenditure.amount-cut_amount)}")

    remaining_gap = max(0,gap-total_cuts-borrow_amount)
    remaining_spending = total_spending-total_cuts
    you_need_header.subheader(f"You need ${human_conceivable_number(remaining_gap,True)}")

    balance_bar.html(
        render_balance_bar(funded=tax_receipts+borrow_amount,
                           gap=remaining_gap,
                           total=remaining_spending
                           ))
    
    