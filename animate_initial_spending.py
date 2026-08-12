import time
import streamlit as st
from pathlib import Path
from etl import Expenditure
from build_spending_boxes import build_spending_boxes

SPENDING_HTML = """
<div id="spending-container"></div>
"""

SPENDING_JS = Path("spending-component.js").read_text()
SPENDING_CSS = Path("style.css").read_text()

spending_component = st.components.v2.component(
    "spending_breakdown",
    html=SPENDING_HTML,
    css=SPENDING_CSS,
    js=SPENDING_JS
)

def animate_initial_spending(
    total_spending: float,
    categories: list[Expenditure],
    animate: bool = True,
    duration: float = 1.2
):
    if animate:
        placeholder = st.empty()

        # Stage 1: one big green spending block
        placeholder.html(
            f"""
            <div style="
                width: 100%;
                height: 72px;
                background: #2ecc71;
                border-radius: 10px;
                box-shadow: 0 6px 0 #1f9d55;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                font-weight: 700;
            ">
                Total spending: ${total_spending:.2f}T
            </div>
            """
        )

        time.sleep(0.8)

        steps = 40

        for step in range(steps + 1):
            progress = step / steps

            boxes_html = build_spending_boxes(categories,progress)
            placeholder.html(boxes_html)

            time.sleep(duration / steps)

        placeholder.empty()
    else:
        boxes_html = build_spending_boxes(
        categories,
        progress=1.0)

    result = spending_component(
        data={"html": boxes_html},
        on_selected_change=lambda: None,
        key="spending_breakdown"
        )

    return result