from dataclasses import dataclass,field
from datetime import date
from typing import Optional

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
    gao_function: GAOFunction | None = None

@dataclass
class ExpenditureDisplay:
    expenditure: Expenditure
    children : list[Expenditure] = field(default_factory=list[Expenditure])

@dataclass
class GAOFunction:
    code: str
    name: str
    description: str
    supercode: str | None = None
    subcodes: list[str]=field(default_factory=list)

@dataclass
class TreasuryYieldCurve:
    date: date
    one_month: Optional [float]
    one_point_five_month: Optional [float]
    two_month: Optional [float]
    three_month: Optional [float]
    four_month: Optional [float]
    six_month: Optional [float]
    one_year: Optional [float]
    two_year: Optional [float]
    three_year: Optional [float]
    five_year: Optional [float]
    seven_year: Optional [float]
    ten_year: Optional [float]
    twenty_year: Optional [float]
    thirty_year: Optional [float]
