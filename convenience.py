from etl.datamodel import GAOFunction

def human_conceivable_number(value):
    abs_value = abs(value*1000000)

    if abs_value >= 1_000_000_000_000:
        retval = f"{abs_value/1_000_000_000_000:,.2f}T"
    elif abs_value >= 1_000_000_000 and abs_value < 1_000_000_000_000:
        retval = f"{abs_value/1_000_000_000:,.2f}B"
    elif abs_value >= 1_000_000 and abs_value < 1_000_000_000:
        retval = f"{abs_value/1_000_000:,.2f}M"
    else:
        retval = f"{abs_value:,.0f}"

    return retval

def gao_lookup(gao_functions: list[GAOFunction],gao_code: str)-> GAOFunction:
     retval = next(
            (
                gao_function
                for gao_function in gao_functions
                if gao_function
                and gao_function.code == gao_code
            ),
            None)
     return retval