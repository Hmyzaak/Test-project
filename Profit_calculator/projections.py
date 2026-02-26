from dataclasses import dataclass
from decimal import Decimal
from typing import List

from models import *


@dataclass
class YearlyProjection:
    year: int
    total_deposited: Decimal
    total_value: Decimal
    entry_value: Decimal
    periodic_value: Decimal
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
        entry_deposit: Deposit,
        periodic_deposit: Deposit,
        inflation_rate: Decimal = Decimal(0),
) -> List[YearlyProjection]:
    projections = []

    for year in range(1, max_years + 1):

        yearly_context = investment_context.with_years(year)

        entry_fv = entry_deposit.calculate_future_value(yearly_context)
        periodic_fv = periodic_deposit.calculate_future_value(yearly_context)
        total_value = entry_fv + periodic_fv

        entry_total = entry_deposit.calculate_total_deposit_amount(yearly_context)
        periodic_total = periodic_deposit.calculate_total_deposit_amount(yearly_context)

        real_value = adjust_for_inflation(total_value, year, inflation_rate)

        projection = YearlyProjection(
            year=year,
            total_value=total_value,
            entry_value=entry_fv,
            periodic_value=periodic_fv,
            total_deposited=entry_total + periodic_total,
            total_value_real=real_value,
        )

        projections.append(projection)

    return projections
