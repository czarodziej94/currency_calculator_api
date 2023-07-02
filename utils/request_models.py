from typing import List

from pydantic import BaseModel


class CurrencyTotalCostRequest(BaseModel):
    currencies: List[str]
    amounts: List[float]
    date: str
