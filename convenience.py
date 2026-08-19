from etl.datamodel import GAOFunction

def human_conceivable_number(value,render_as_word:bool=False):
    abs_value = abs(value*1_000_000)

    units = [
        (1_000_000_000_000, "T", "Trillion"),
        (1_000_000_000, "B", "Billion"),
        (1_000_000, "M","Million"),
        (1_000,"K","Thousand")
    ]

    for divisor,short,word in units:
        if abs_value >= divisor:
            suffix = word if render_as_word else short
            number = value * 1_000_000 /divisor
            return f"{number:.2f} {suffix}"

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