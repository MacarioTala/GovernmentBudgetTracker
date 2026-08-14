import time
import streamlit as st
from convenience import human_conceivable_number
from animate_bar.render_expanding_bar import render_expanding_bar
from animate_bar.render_final_bar import render_final_bar


def animate_bar(
    label,
    amount,
    max_amount,
    threshold=None,
    duration=1.5
):
    ''' animate_bar depends on html rendered by the two subfunctions: 
        render_expanding_bar and render_final_bar
        this is used to generate the animation of the budget intro
        and any bar that needs a horizontal stacked bar
    '''
    placeholder = st.empty()
    steps = 60
    final_width = 85
    shrink_steps = 15

    def render_gap(amount:int):
        if amount>0:
            return f"Gap: ${human_conceivable_number(amount)}"
        else:
            return ""

    for step in range(steps + 1):
        progress = step / steps
        current_amount = amount * progress

        if threshold is None:
            green_amount = current_amount
            red_amount = 0
        else:
            green_amount = min(current_amount, threshold)
            red_amount = max(0, current_amount - threshold)

        green_width = green_amount / max_amount * 100
        red_width = red_amount / max_amount * 100

        html = render_expanding_bar(label,current_amount,green_width,red_width)

        placeholder.html(html)

        time.sleep(duration / steps)

    for step in range(shrink_steps + 1):
        progress = step / shrink_steps

        container_width = 100 - ((100 - final_width) * progress)

        green_amount = min(amount, threshold) if threshold else amount
        red_amount = max(0, amount - threshold) if threshold else 0

        green_width = green_amount / max_amount * 100
        red_width = red_amount / max_amount * 100

        html = render_final_bar(label,amount,container_width,green_width,red_width,render_gap(red_amount))

        placeholder.html(html)

        time.sleep(0.01)