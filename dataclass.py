from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExpenseData:
    id: int = 0
    user_id: int = 0
    name: str = None
    amount: float = 0.0
    split_type: str = None
    open: bool = False
    date: datetime = datetime.today()

    def __repr__(self):
        return f"{self.name} {self.amount}"
