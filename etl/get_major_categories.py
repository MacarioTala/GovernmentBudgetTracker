from etl.datamodel import Expenditure,ExpenditureDisplay,GAOFunction
import streamlit as st


@st.cache_data
def get_major_categories(expenditures:list[Expenditure],threshold:int)-> list[ExpenditureDisplay]:
    """
    Returns each major expenditure, as defined by being >= threshold as one ExpenditureDisplay
    and consolidates the rest as 'Others' 
    """
    SYNTHETIC_GAO_OTHERS = "__OTHERS__"
    SYNTHETIC_GAO_UOR = "__UOR__"
    top_level_functions = [
        x for x in expenditures
        if x.level==1
        or x.name == "National Defense"
        or x.name == "Net interest"
        or (x.name == "Undistributed offsetting receipts" and x.level==0)
    ]

    functions = sorted(
        top_level_functions,
        key= lambda x: x.amount,
        reverse=True)

    major_categories = [
        ExpenditureDisplay
        (
                expenditure=x,
                children=[]#major categories have no children
             )
            for x in functions
            if x.percentage >= threshold
        ]

    synthetic_other_function = GAOFunction(code=SYNTHETIC_GAO_OTHERS,name="Other",description="Spending categories comprising<10% of the budget")
    synthetic_uor_function = GAOFunction(code=SYNTHETIC_GAO_UOR,name = "Undistributed offsetting receipts", description="The government's equivalent of finding a 20 in your pocket")

    other_expenditure = ExpenditureDisplay(
        expenditure =  Expenditure(
            name="Others",
            amount=sum(x.amount for x in functions if x.percentage < threshold and x.amount > 0),
            percentage=sum(x.percentage for x in functions if x.percentage<threshold and x.amount > 0),
            gao_function=synthetic_other_function,
            level=0),
        children = [x for x in functions if x.percentage < threshold and x.amount > 0])
    
    uor_expenditure = ExpenditureDisplay(
        expenditure = Expenditure(
             name="UOR",
             amount=sum(x.amount for x in functions if x.amount<0),
             percentage=sum(x.percentage for x in functions if x.amount<0),
             level=0,
             gao_function=synthetic_uor_function
         ),
        children = []
         )

    major_categories.append(other_expenditure)
    major_categories.append(uor_expenditure)

    return major_categories