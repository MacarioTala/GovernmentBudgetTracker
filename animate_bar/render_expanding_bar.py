import textwrap
from convenience import human_conceivable_number

def render_expanding_bar(
        label : str,
        amount: int,
        green_width : int,
        red_width : int):
    return textwrap.dedent(f"""
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
                ${human_conceivable_number(amount)}
            </div>
        </div>
        """)