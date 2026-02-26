from models import *
from projections import generate_yearly_projection
from retirement import simulate_withdrawal_until_depleted


snp_etf = InvestmentContext(18, 0.08, CompoundingFrequency.PER_DIEM, 0.0003, InterestType.NOMINAL, 0.0)
vstupni_vklad = Deposit(DepositType.ENTRY, 0, 0, 0.0015, FeeType.PROPORTIONAL, AnnuityType.DUE,)
periodicky_vklad = Deposit(DepositType.PERIODIC, 2000, 12, 0.0015, FeeType.PROPORTIONAL, AnnuityType.DUE,)

vyrocni_prispevek = Deposit(DepositType.PERIODIC, 2000, 1, 0, FeeType.PROPORTIONAL, AnnuityType.ORDINARY)

projections = generate_yearly_projection(snp_etf.years, snp_etf, vstupni_vklad, periodicky_vklad, Decimal(0.02),)

for p in projections:
      print(f'Pro rok {p.year} vloženo {int(p.total_deposited)} CZK a naspořeno {int(p.total_value)} CZK - reálná kupní síla: {int(p.total_value_real)} CZK.')


"""
real_capital = projections[-1].total_value_real
withdrawal_simulation = simulate_withdrawal_until_depleted(
      initial_capital=real_capital,
      withdrawal_amount=Decimal(20000),
      withdrawals_per_year=12,
      context=investice,
)
print(f'Kapitál vydrží {withdrawal_simulation[-1].year} let při výběru {withdrawal_simulation[0].withdrawal} CZK.')
"""