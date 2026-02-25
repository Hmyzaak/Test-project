from models import *
from projections import generate_yearly_projection

investice = InvestmentContext(20, 0.05,CompoundingFrequency.PER_MENSEM,InterestType.NOMINAL,0.0003,)
vstupni_vklad = Deposit(DepositType.ENTRY, 5000, 0, AnnuityType.DUE, 0.0015, FeeType.PROPORTIONAL,)
periodicky_vklad = Deposit(DepositType.PERIODIC, 1000, 12, AnnuityType.DUE, 0.0015, FeeType.PROPORTIONAL,)

projections = generate_yearly_projection(20, investice, vstupni_vklad, periodicky_vklad,)

for p in projections:
      print(f'Pro rok {p.year} vloženo {int(p.total_deposited)} CZK a naspořeno {int(p.total_value)} CZK.')

