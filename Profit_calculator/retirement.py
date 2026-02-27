from dataclasses import dataclass
from decimal import Decimal
from typing import List

from models import InvestmentContext, FeeType


@dataclass
class WithdrawalPeriod:
    period: int
    year: int
    capital_start: Decimal
    withdrawal: Decimal
    fee: Decimal
    capital_end: Decimal


def simulate_withdrawal_until_depleted(
    initial_capital: Decimal,
    withdrawal_amount: Decimal,
    withdrawals_per_year: int,
    context: InvestmentContext,
    fee_amount: Decimal = Decimal(0),
    fee_type: FeeType = FeeType.FIXED,
) -> List[WithdrawalPeriod]:

    capital = initial_capital
    periodic_rate = context.calculate_periodic_interest_rate()

    results = []
    period = 0

    while capital > 0:
        period += 1
        year = (period - 1) // withdrawals_per_year + 1

        capital_start = capital

        # úročení
        capital *= (Decimal(1) + periodic_rate)
        # poplatek
        if fee_type == FeeType.PROPORTIONAL:
            fee = withdrawal_amount * fee_amount
        else:
            fee = fee_amount

        total_withdrawal = withdrawal_amount + fee

        # pokud by poslední výběr překročil kapitál, vybere se jen to, co zbývá (poplatek se ruší)
        if total_withdrawal > capital:
            total_withdrawal = capital
            fee = Decimal(0)

        capital -= total_withdrawal

        results.append(
            WithdrawalPeriod(
                period=period,
                year=year,
                capital_start=capital_start,
                withdrawal=withdrawal_amount,
                fee=fee,
                capital_end=capital,
            )
        )

        if capital <= 0:
            break
        # Zbytečné, ale pojistka pro while cyklus

    return results
