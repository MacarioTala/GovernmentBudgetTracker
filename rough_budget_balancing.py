import streamlit as st
from convenience import human_conceivable_number
from etl.datamodel import ExpenditureDisplay
from budget_balancing.render_balance_bar import render_balance_bar
from dataclasses import dataclass
from add_new_program import add_new_program

@dataclass 
class Cut:
     name: str
     percentage : int
     amount : int

def rough_budget_balancing(tax_receipts: int
                           , expenditure_displays : list[ExpenditureDisplay]
                           , one_year_yield: float
                           , thirty_year_yield: float
                           ):

    if "budget_screen" not in st.session_state:
         st.session_state.budget_screen = "editor"

    if "financing_next_year" not in st.session_state:
         st.session_state.financing_next_year = None

    if "financing_long_term" not in st.session_state:
             st.session_state.financing_long_term = None

    new_programs = st.session_state.get("new_programs",[])
    all_expenditure_displays = expenditure_displays+new_programs
    new_spending = sum(display.expenditure.amount
                           for display in new_programs)
    total_spending= sum(display.expenditure.amount
                           for display in all_expenditure_displays)
    total_cuts=0
    cuts_made:list[Cut]=[]
    gap=max(0,total_spending-tax_receipts)
    remaining_gap=gap

    yn_column,btn_new_program_column,btn_finalize_column = st.columns([.74,.13,.13])
    with yn_column:
        you_need_header=st.empty()
        if not st.session_state.budget_screen == "summary":
            st.caption("You can see the effect of adding new spending to this by clicking 'Add New Program'")

    with btn_new_program_column:
         if not st.session_state.budget_screen == "summary":
            if st.button("Add New Program"):
                add_new_program(total_spending)

    with btn_finalize_column:
         if not st.session_state.budget_screen == "summary":
            finalize_clicked = st.button("Finalize Budget ->")

    finalize_message = st.empty()
    balance_bar = st.empty()

    if st.session_state.budget_screen == "summary":
        st.header("You balanced the budget!")

        if st.session_state.new_programs:
             st.write(f"- You added the following new programs, totalling {human_conceivable_number(new_spending)}")
             _,new_program_column= st.columns([.05,.95])
             with new_program_column:
                  for program in st.session_state.new_programs:
                       st.write(f"- {program.expenditure.name} : {human_conceivable_number(program.expenditure.amount)}")
        if st.session_state.final_total_cuts:
            st.write(f"- You cut **${human_conceivable_number(st.session_state.final_total_cuts)}**")
            st.write(f"Consisting of:")
            _,cut_column = st.columns([.05,.95])
            with cut_column:
                for cut in st.session_state.final_cuts_made:
                    st.write(f"- Cutting {cut.name} by {cut.percentage}%, saving **${human_conceivable_number(cut.amount)}**")
        else:
             st.write("- You cut nothing from the budget")
        if human_conceivable_number(st.session_state.borrow_amount_final) is not None:
            st.write(f"- You borrowed **${human_conceivable_number(st.session_state.borrow_amount_final)}**")
            st.write(f"- Your borrowing has increased next year's deficit by: ${human_conceivable_number(st.session_state.financing_next_year)}")
        if st.session_state.financing_long_term:
            st.write(f"... and a total of ${human_conceivable_number(st.session_state.financing_long_term)} over the next 30 years") 
        st.write(f"Thanks for trying Balance the Budget!")
        st.write(f"V3 will let you cut specific programs")

        st.caption(f"*For information and educational purposes only. Congress isn't mucking around with sliders for the budget")

        if st.button("Try Again"):
             st.session_state.clear()
             st.rerun()
        return

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
            if human_conceivable_number(borrow_amount) is not None:
                st.write(f"**${human_conceivable_number(borrow_amount)}**")

    st.write(f"Currently borrowing {human_conceivable_number(borrow_amount)} which is {borrow_percentage}% of the budget gap: " if human_conceivable_number(borrow_amount) is not None else "")
    _,disclaimer = st.columns([.05,.95])
    with disclaimer:
        if borrow_amount is not None and borrow_amount != 0:
            SHORT="Short-term"
            LONG ="Long-term"
            st.write("Do you want to borrow:")
            borrow_term = st.segmented_control(
                         "Borrow Term",
                         [SHORT,LONG],
                         default="Short-term",
                         label_visibility="collapsed"
                    )
            if borrow_term == SHORT:
                new_short_borrowing = borrow_amount*one_year_yield
                st.session_state.financing_next_year=new_short_borrowing
                st.write(f"- This borrowing will add ${human_conceivable_number(new_short_borrowing)} to next year's Net Interest Expense")
            else:
                new_short_borrowing=borrow_amount*thirty_year_yield
                st.session_state.financing_next_year=new_short_borrowing
                new_long_borrowing=borrow_amount*thirty_year_yield*30
                st.session_state.financing_long_term=new_long_borrowing
                st.write(f"- This borrowing will add ${human_conceivable_number(new_short_borrowing)} a year to the Net Interest Expense for the next 30 years")
                st.write(f"   ... or ${human_conceivable_number(new_long_borrowing)} over the next 30 years")
            
            st.caption(f"*Note: This is a highly simplified version of the debt process. It is accurate to the nearest million, but actual costs depend on issuance, refinancing, and future interest rates")
        else:
             st.write("You are borrowing nothing for next year")
         
    for display in all_expenditure_displays:
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

            if cut_amount>0:
                 cuts_made.append(
                      Cut(
                           display.expenditure.name,
                           cut_percentage,
                           cut_amount
                           )
                 )
            st.session_state.final_cuts_made = cuts_made
            
        with label_column:
                    st.write(f"{display.expenditure.name}")
                    st.caption(f"${human_conceivable_number(display.expenditure.amount-cut_amount)}")

    remaining_gap = max(0,gap-total_cuts-borrow_amount)
    remaining_spending = total_spending-total_cuts
    you_need_header.subheader(f"You need ${human_conceivable_number(remaining_gap,True)}")

    if finalize_clicked:
        st.session_state.finalize_clicked = False
        if remaining_gap > 0:
            finalize_message.error("You have not balanced the budget!")
        else:
            st.session_state.borrow_amount_final = borrow_amount
            st.session_state.final_total_cuts = total_cuts
            st.session_state.budget_screen = "summary"
            st.session_state.final_borrow_amount = borrow_amount
            st.session_state.final_total_cuts = total_cuts
            st.rerun()

    balance_bar.html(
        render_balance_bar(funded=tax_receipts+borrow_amount,
                           gap=remaining_gap,
                           total=remaining_spending
                           ))