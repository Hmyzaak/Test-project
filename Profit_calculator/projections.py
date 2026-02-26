from dataclasses import dataclass
from decimal import Decimal
from typing import List

from models import *


@dataclass
class YearlyProjection:
    year: int
    total_deposited: Decimal
    total_value_nominal: Decimal
    total_value_real: Decimal


def adjust_for_inflation(
        nominal_value: Decimal,
        years: int,
        annual_inflation_rate: Decimal,
) -> Decimal:

    if annual_inflation_rate <= 0:
        return nominal_value

    inflation_factor = (Decimal(1) + annual_inflation_rate) ** years
    return nominal_value / inflation_factor


def generate_yearly_projection(
        max_years: int,
        investment_context: InvestmentContext,
        deposits: List[Deposit],
        inflation_rate: Decimal = Decimal(0),
) -> List[YearlyProjection]:
    projections = []

    for year in range(1, max_years + 1):

        yearly_context = investment_context.with_years(year)

        total_deposited = Decimal(0)
        total_value_nominal = Decimal(0)

        for deposit in deposits:
            total_deposited += deposit.calculate_total_deposit_amount(yearly_context)
            total_value_nominal += deposit.calculate_future_value(yearly_context)

        real_value = adjust_for_inflation(total_value_nominal, year, inflation_rate)

        projection = YearlyProjection(
            year=year,
            total_deposited=total_deposited,
            total_value_nominal=total_value_nominal,
            total_value_real=real_value,
        )

        projections.append(projection)

    return projections
