import time
import textwrap
import streamlit as st


def animate_bar(
    label,
    amount,
    max_amount,
    threshold=None,
    duration=1.5
):
    placeholder = st.empty()
    steps = 60
    final_width = 85
    shrink_steps = 15

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

        html = textwrap.dedent(f"""
<div style="margin-bottom: 6px; font-weight: 700">{label}</div>

        <div style="
            width: 100%;
            height: 42px;
            background: #e6e6e6;
            border-radius: 6px;
            overflow: hidden;
            position: relative;
        ">
            <div style="
                position: absolute;
                left: 0;
                width: {green_width}%;
                height: 100%;
                background: #2ecc71;
            "></div>

            <div style="
                position: absolute;
                left: {green_width}%;
                width: {red_width}%;
                height: 100%;
                background: #e74c3c;
            "></div>

            <div style="
                position: absolute;
                left: 12px;
                top: 0;
                height: 100%;
                display: flex;
                align-items: center;
                color: white;
                font-weight: 600;
                font-size: 18px;
            ">
                ${current_amount:.2f}T
            </div>
        </div>
        """)

        placeholder.html(html)

        time.sleep(duration / steps)

    for step in range(shrink_steps + 1):
        progress = step / shrink_steps

        container_width = 100 - ((100 - final_width) * progress)

        green_amount = min(amount, threshold) if threshold else amount
        red_amount = max(0, amount - threshold) if threshold else 0

        green_width = green_amount / max_amount * 100
        red_width = red_amount / max_amount * 100

    html = f"""
<div style="
    width: {container_width}%;
    height: 28px;
    background: #e6e6e6;
    border-radius: 5px;
    overflow: hidden;
    position: relative;
">
    <div style="
        position: absolute;
        left: 0;
        width: {green_width}%;
        height: 100%;
        background: #2ecc71;
    "></div>

    <div style="
        position: absolute;
        left: {green_width}%;
        width: {red_width}%;
        height: 100%;
        background: #e74c3c;
    "></div>

    <div style="
        position: absolute;
        left: 10px;
        top: 0;
        height: 100%;
        display: flex;
        align-items: center;
        color: white;
        font-weight: 600;
        font-size: 14px;
    ">
       {label} ${amount:.2f}T
    </div>
</div>
"""

    placeholder.html(html)

    time.sleep(0.01)