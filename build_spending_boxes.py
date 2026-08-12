from etl import Expenditure

def build_spending_boxes(
    categories: list[Expenditure],
    progress: float
):
    boxes = ""

    for category in categories:
        width = abs(category.percentage) * progress

        is_uor = category.name == "UOR"

        label = "UOR" if is_uor else category.name
        background = "#2980b9" if is_uor else "#2ecc71"

        tooltip = (
            "Undistributed Offsetting Receipts are the government's "
            "equivalent of finding some loose change under the couch"
            if is_uor
            else category.name
        )

        boxes += f"""
        <button
            class="budget-box"
            data-category="{category.name}"
            title="{tooltip}"
            style="
                width: {width}%;
                min-width: {"55px" if is_uor else "0"};
                height: 90px;
                background: {background};
                border: none;
                border-right: 2px solid white;
                padding: 0;
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
                cursor: pointer;
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
        </button>
        """

    return f"""
    <div style="
        display: flex;
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
    ">
        {boxes}
    </div>
    """