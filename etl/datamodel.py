from dataclasses import dataclass,field

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