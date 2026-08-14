from convenience import human_conceivable_number

def render_final_bar(
        label:str,
        amount: int,
        container_width: int,
        green_width: int,
        red_width: int,
        gap_text: str
):
    return f"""
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
        overflow: hidden;
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
       {label} ${human_conceivable_number(amount)}
    </div>
     <div style="
            position: absolute;
            justify-content: center;
            left: {green_width}%;
            width: {red_width}%;
            top: 0;
            height: 100%;

            display: flex;
            align-items: center;
            padding-left: 10px;
            box-sizing: border-box;

            overflow:hidden;
            white-space: nowrap;

            color: white;
            font-weight: 600;
            font-size: 14px;
        ">
            {gap_text}
        </div>
</div>
"""