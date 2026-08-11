import time
import streamlit as st

def animate_spending_breakdown(
    total_spending: float,
    categories: list,
    duration: float = 1.2
):
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

        boxes = ""

        for category in categories:
            # Use absolute percentage so UOR gets visible width
            width = abs(category.percentage) * progress

            is_uor = category.name == "Undistributed offsetting receipts"

            label = "UOR" if is_uor else category.name

            background = "#2980b9" if is_uor else "#2ecc71"

            tooltip = (
                "Undistributed Offsetting Receipts are the government's "
                "equivalent of finding some loose change under the couch"
                if is_uor
                else category.name
            )

            boxes += f"""
            <div
                title="{tooltip}"
                style="
                    width: {width}%;
                    min-width: {"55px" if is_uor else "0"};
                    height: 90px;
                    background: {background};
                    border-right: 2px solid white;
                    box-sizing: border-box;

                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;

                    color: white;
                    font-weight: 700;
                    text-align: center;

                    box-shadow: inset 0 -6px 0 rgba(0,0,0,0.15);

                    overflow: hidden;
                "
            >
                <div>{label}</div>
                <div style="
                    font-size: 13px;
                    font-weight: 500;
                    margin-top: 4px;
                ">
                    {category.percentage:.1f}%
                </div>
            </div>
            """

        placeholder.html(
            f"""
            <div style="
                display: flex;
                width: 100%;
                border-radius: 10px;
                overflow: hidden;
            ">
                {boxes}
            </div>
            """
        )

        time.sleep(duration / steps)