from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from datetime import datetime

from db.database import get_db
from db.models import ExchangeRate
from utils.nbp_api import fetch_exchange_sell_rate, fetch_exchange_mid_rate
from utils.request_models import CurrencyTotalCostRequest


router = APIRouter()


@router.get("/exchange_rate")
async def get_exchange_rate(currency: str,
                            date: str = datetime.now().strftime("%Y-%m-%d"),
                            db: Session = Depends(get_db)):
    exchange_rate = db.query(ExchangeRate).filter_by(currency=currency, date=date).first()

    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()  # convert string to date object
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date.")

    if exchange_rate is None:
        exchange_rate_data = fetch_exchange_sell_rate(currency, date.strftime("%Y-%m-%d"))

        if exchange_rate_data is None:
            raise HTTPException(status_code=404, detail="Exchange rates not found.")

        new_exchange_rate = ExchangeRate(
            currency=currency,
            date=date,
            rate=exchange_rate_data['sell']
        )
        db.add(new_exchange_rate)
        db.commit()
        db.refresh(new_exchange_rate)

        return {f"{str(new_exchange_rate.currency)}/PLN": new_exchange_rate.rate,
                "date": new_exchange_rate.date}
    else:
        return {f"{str(exchange_rate.currency)}/PLN": exchange_rate.rate,
                "date": exchange_rate.date}


@router.post("/total_cost")
async def calculate_total_cost(request_data: CurrencyTotalCostRequest = Body(...)):
    currencies = request_data.currencies
    amounts = request_data.amounts
    date = request_data.date if request_data.date else datetime.now().strftime("%Y-%m-%d")

    if len(currencies) != len(amounts):
        raise HTTPException(status_code=400, detail="The number of currencies and amounts must match.")
    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()  # convert string to date object
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date.")

    total_cost = 0.0
    currencies__with_amount = []

    for currency, amount in zip(currencies, amounts):
        exchange_rate_data = fetch_exchange_mid_rate(currency, date.strftime("%Y-%m-%d"))

        if exchange_rate_data is None:
            raise HTTPException(status_code=404, detail=f"Exchange rate for currency {currency} not found.")

        exchange_rate = exchange_rate_data["mid"]
        currencies__with_amount.append(f"{amount} {currency}")
        cost = exchange_rate * amount
        total_cost += cost

    return {"entered": ' + '.join(currencies__with_amount),
            "total_cost": total_cost,
            "date": date}


@router.get("/")
async def root():
    return {"message": "Hello World"}