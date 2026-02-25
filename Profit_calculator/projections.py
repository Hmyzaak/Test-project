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


def generate_yearly_projection(
        max_years: int,
        investment_context: InvestmentContext,
        entry_deposit: Deposit,
        periodic_deposit: Deposit,
) -> List[YearlyProjection]:
    projections = []

    for year in range(1, max_years + 1):

        yearly_context = investment_context.with_years(year)

        entry_fv = entry_deposit.calculate_future_value(yearly_context)
        periodic_fv = periodic_deposit.calculate_future_value(yearly_context)
        entry_total = entry_deposit.calculate_total_deposit_amount(yearly_context)
        periodic_total = periodic_deposit.calculate_total_deposit_amount(yearly_context)

        projection = YearlyProjection(
            year=year,
            total_deposited=entry_total + periodic_total,
            total_value=entry_fv + periodic_fv,
            entry_value=entry_fv,
            periodic_value=periodic_fv,
        )

        projections.append(projection)

    return projections
