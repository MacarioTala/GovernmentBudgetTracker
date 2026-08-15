from pathlib import Path
from convenience import human_conceivable_number

def render_balance_bar(funded: int, gap: int, total: int):

    BALANCE_BAR_HTML = Path("budget_balancing/render_balance_bar.html").read_text()
    return BALANCE_BAR_HTML.format(
        funded_width = funded/total * 100,
        gap_width = gap/total * 100,
        gap = human_conceivable_number(gap)
    )