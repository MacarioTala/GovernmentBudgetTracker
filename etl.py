
import pandas as pd
from dataclasses import dataclass
from io import BytesIO
from openpyxl import load_workbook
import requests

@dataclass
class Budget:
    year : int
    receipts: int
    outlays : int
    deficit : int 

@dataclass
class Expenditure:
    name : str
    amount : int
    percentage : float
    level : int


def get_budget_data()-> Budget:
    dataset_url = "https://www.govinfo.gov/content/pkg/BUDGET-2027-TAB/xls/BUDGET-2027-TAB-2-1.xlsx"
    df = pd.read_excel(dataset_url)
    latest = df.dropna(subset=[df.columns[1]]).iloc[-1]
    return Budget(
        year=int(latest.iloc[0]),
        receipts=int(latest.iloc[1]),
        outlays=int(latest.iloc[2]),
        deficit=int(latest.iloc[3])
    )

def get_expenditure_by_function(budget_total: int,year:int = 2025)-> list[Expenditure]:
    dataset_url = (
        "https://www.govinfo.gov/content/pkg/"
        "BUDGET-2027-TAB/xls/BUDGET-2027-TAB-4-1.xlsx"
        )
    response = requests.get(dataset_url,timeout=30)
    wb=load_workbook(BytesIO(response.content))
    ws=wb.active
    
    year_column = None
    for cell in ws[2]:
        if cell.value == str(year):
            year_column = cell.column
            break
    if year_column is None:
        raise ValueError(f"Year {year} not found in expenditure table")

    expenditures = []

    for row in range(4, ws.max_row + 1):
        name_cell = ws.cell(row=row, column=1)

        if name_cell.value == "As percentages of outlays:":
            break

        amount_cell = ws.cell(row=row, column=year_column)

        name = name_cell.value
        amount = amount_cell.value

        if name is None:
            continue

        if amount is None or str(amount).strip(". ") == "":
            amount = 0

        expenditures.append(
            Expenditure(
                name=str(name),
                amount=int(amount),
                percentage=(int(amount) / budget_total) * 100,
                level=int(name_cell.alignment.indent or 0)
            )
        )
    
    return expenditures

def get_major_categories(expenditures:list[Expenditure])-> list[Expenditure]:
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
        x
        for x in functions
        if x.percentage >= 10 
    ]

    categories_in_others = [
        x for x in functions
        if x.percentage<10
        ]
    
    other_amount = sum(x.amount 
                       for x in categories_in_others
                       if x.amount>0)
    other_percentage = sum(x.percentage 
                           for x in categories_in_others
                           if x.amount>0)

    other_expenditure = Expenditure(
        name="Others",
        amount=other_amount,
        percentage=other_percentage,
        level=0
    )

    uor_amount = sum(x.amount
                             for x in categories_in_others
                             if x.amount<0)

    uor_percentage = sum(x.percentage 
                                 for x in categories_in_others 
                                 if x.amount<0)

    uor_expenditure = Expenditure(
        name="Undistributed offsetting receipts",
        amount=uor_amount,
        percentage=uor_percentage,
        level=0
    )
    
    major_categories.append(other_expenditure)
    major_categories.append(uor_expenditure)

    return major_categories

    


#%%
from etl import get_budget_data
from etl import get_expenditure_by_function
from etl import get_major_categories
budget_total = get_budget_data().outlays
expenditures = get_expenditure_by_function(budget_total)
major_categories = get_major_categories(expenditures)

for x in major_categories:
    print(f"{x.name:<55} : {x.percentage:>6.2f} %")
# %%
