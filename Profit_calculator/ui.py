from models import *
from projections import generate_yearly_projection
from retirement import simulate_withdrawal_until_depleted

annual_inflation_rate = Decimal("0.02")

snp_etf = InvestmentContext(18, 0.10, CompoundingFrequency.PER_DIEM, 0.0003, InterestType.EFFECTIVE, 0)
vstupni_vklad = Deposit(DepositType.ENTRY, 0, 0, 0.0015, FeeType.PROPORTIONAL, AnnuityType.DUE)
periodicky_vklad = Deposit(DepositType.PERIODIC, 12000, 12, 0.0015, FeeType.PROPORTIONAL, AnnuityType.DUE)

projections = generate_yearly_projection(snp_etf.years, snp_etf, [vstupni_vklad, periodicky_vklad], annual_inflation_rate,)
for p in projections:
      print(f'Pro rok {p.year} vloženo {int(p.total_deposited)} CZK a naspořeno {int(p.total_value_nominal)} CZK - reálná kupní síla: {int(p.total_value_real)} CZK.')

"""
print('\n')

sporeni = InvestmentContext(18, 0.05, 1, 0.015, InterestType.NOMINAL, Decimal(0))
iniciace_sporeni = Deposit(DepositType.ENTRY, 1000, 0, 0, FeeType.FIXED, AnnuityType.DUE)
periodicke_sporeni = Deposit(DepositType.PERIODIC, 2000, 12, 0, FeeType.FIXED, AnnuityType.DUE)
vyrocni_prispevek = Deposit(DepositType.PERIODIC, 2000, 1, 0, FeeType.PROPORTIONAL, AnnuityType.ORDINARY)

projections = generate_yearly_projection(sporeni.years, sporeni, [iniciace_sporeni, periodicke_sporeni, vyrocni_prispevek], Decimal(0.02))
for p in projections:
      print(f'Pro rok {p.year} vloženo {int(p.total_deposited)} CZK a naspořeno {int(p.total_value_nominal)} CZK - reálná kupní síla: {int(p.total_value_real)} CZK.')
"""

withdrawal_amount = Decimal("20000")
real_capital = projections[-1].total_value_real
withdrawal_simulation = simulate_withdrawal_until_depleted(
      initial_capital=real_capital,
      withdrawal_amount=withdrawal_amount,
      withdrawals_per_year=12,
      annual_inflation_rate=annual_inflation_rate,
      context=snp_etf,
)
print(f'Kapitál vydrží {withdrawal_simulation[-1].year} let při výběru {withdrawal_amount} CZK.')
