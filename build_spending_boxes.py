from etl.datamodel import ExpenditureDisplay
import streamlit as st

def build_spending_boxes(
    categories: list[ExpenditureDisplay],
    progress: float
):
    boxes = ""
    for category in categories:
        width = abs(category.expenditure.percentage) * progress

        is_uor = category.expenditure.name == "UOR"

        label = "UOR" if is_uor else category.expenditure.name
        background = "#2980b9" if is_uor else "#2ecc71"

        tooltip = (
            "Undistributed Offsetting Receipts are the government's "
            "equivalent of finding some loose change under the couch"
            if is_uor
            else category.expenditure.name
        )

        boxes += f"""
        <button
            class="budget-box"
            data-category="{category.expenditure.name}"
            data-gaocode ="{category.expenditure.gao_function.code if category.expenditure.gao_function else ''}"
            title="{tooltip}"
            style="
                width: {width}%;
                min-width: {"55px" if is_uor else "0"};
                background: {background};
            "
        >
            <div>{label}</div>
            <div style="
                font-size: 13px;
                font-weight: 500;
                margin-top: 4px;
            ">
                {category.expenditure.percentage:.1f}%
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