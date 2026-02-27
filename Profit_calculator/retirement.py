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
    annual_inflation_rate: Decimal,
    context: InvestmentContext,
    fee_amount: Decimal = Decimal(0),
    fee_type: FeeType = FeeType.FIXED,
) -> List[WithdrawalPeriod]:

    # reálný kapitál - kupní síla naspořených financí
    capital = initial_capital
    # úroková sazba pro kapitalizační periodu
    periodic_compounding_interest_rate = context.calculate_periodic_interest_rate()
    # počet period pro úročení ku periodě výběru
    compounding_periods_per_withdrawal_period = context.compounding_per_year / withdrawals_per_year
    # poměrná část roční inflace (sazba roční inflace je efektivní) ku periodě výběru
    periodic_inflation_rate = (Decimal(1) + annual_inflation_rate) ** (Decimal(1) / Decimal(withdrawals_per_year)) - Decimal(1)
    # vybíraný obnos zvýšený o poměrnou část roční inflace ku periodě výběru (aby byla vybírána částka o stále stejné kupní síle)
    updated_withdrawal_amount = withdrawal_amount

    # výsledky simulace
    results = []
    # počet provedených výběrů
    withdrawal_periods_done = 0

    while capital > 0:
        withdrawal_periods_done += 1
        year = (withdrawal_periods_done - 1) // withdrawals_per_year + 1

        # úročení
        capital_start = capital
        capital *= ((Decimal(1) + Decimal(periodic_compounding_interest_rate)) ** Decimal(compounding_periods_per_withdrawal_period))
        capital /= (Decimal(1) + periodic_inflation_rate)
        capital_before_withdrawal = capital
        updated_withdrawal_amount *= (Decimal(1) + periodic_inflation_rate)

        # poplatek
        if fee_type == FeeType.PROPORTIONAL:
            fee = updated_withdrawal_amount * fee_amount
        else:
            fee = fee_amount

        total_withdrawal = updated_withdrawal_amount + fee

        # pokud by poslední výběr překročil kapitál, vybere se jen to, co zbývá (poplatek se přepisuje, aby smyčka nepokračovala do záporu)
        if total_withdrawal > capital:
            total_withdrawal = capital
            fee = Decimal(0)

        capital -= total_withdrawal

        results.append(
            WithdrawalPeriod(
                period=withdrawal_periods_done,
                year=year,
                capital_start=capital_start,
                withdrawal=updated_withdrawal_amount,
                fee=fee,
                capital_end=capital,
            )
        )

        if capital <= 0:
            break
        # Zbytečné, ale pojistka pro while cyklus
        if capital > capital_start:
            loop_amount = int(capital_before_withdrawal - capital)
            print(f"Nekonečný cyklus generující stálou rentu. Následující věta nezobrazuje pravdivý počet let, ale to, že již v roce 1 bylo dosaženo podmínky pro nekonečnou smyčku - perioda určená pro výběr renty generuje příjem {loop_amount} CZK.")
            break

    return results
