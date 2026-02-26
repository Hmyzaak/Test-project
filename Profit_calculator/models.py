from enum import Enum
from decimal import Decimal


class InterestType(str, Enum):
    # "nominal" interest type represents the annual interest rate without capitalization frequency for compound interest
    # "effective" interest type represents the annual interest rate including the capitalization frequency for compound interest
    NOMINAL = "nominal"
    EFFECTIVE = "effective"


class CompoundingFrequency(int, Enum):
    # Interest capitalization rate max. 365x per year = every day; min. 1x per year
    PER_ANNUM = 1       # p.a.
    PER_SEMESTRE = 2    # p.s.
    PER_QUARTALE = 4    # p.q.
    PER_MENSEM = 12     # p.m.
    PER_DIEM = 365      # p.d.


class AnnuityType(str, Enum):
    # "due" = deposit is added at beginning of period; "ordinary" = deposit is added at the end of period
    DUE = "due"
    ORDINARY = "ordinary"


class DepositType(str, Enum):
    # Deposit is added periodically or just once at the beginning of investment
    ENTRY = "entry"
    PERIODIC = "periodic"


class FeeType(str, Enum):
    # Fee is "fixed" value independent of the deposit amount or "proportional" to the deposit amount
    PROPORTIONAL = "proportional"
    FIXED = "fixed"


class InvestmentContext:
    def __init__(
        self,
        years: int,
        annual_interest_rate: int,
        compounding_per_year: CompoundingFrequency,
        ter_fee: int,
        interest_type: InterestType = InterestType.NOMINAL,
        tax_interest_rate: Decimal = Decimal(0.15),
    ):
        self.years = years
        self.annual_interest_rate = Decimal(annual_interest_rate)
        self.compounding_per_year = compounding_per_year
        self.ter_fee = Decimal(ter_fee)
        self.interest_type = interest_type
        self.tax_interest_rate = Decimal(tax_interest_rate)
        # Annual tax rate of interests (in CZE it is 0,15), for ETFs after time-test it is 0.

    def __str__(self):
        # Annotation of investment in CZE
        return print(f'Investice na {self.years} let s úrokem {self.annual_interest_rate} kapitalizovaným {self.compounding_per_year}-krát ročně a ročním poplatkem {self.ter_fee}.')

    def calculate_annual_interest_rate(self):
        # Invalid input
        if self.annual_interest_rate <= 0:
            raise ValueError("annual_interest_rate must be grater than 0")
        annual_rate = self.annual_interest_rate
        # Apply TER on annual level (reduces gross return)
        if self.ter_fee > 0:
            annual_rate = (Decimal(1) + annual_rate) * (Decimal(1) - self.ter_fee) - Decimal(1)
        # Apply annual tax rate of interests on profit
        if self.tax_interest_rate > 0:
            annual_rate = annual_rate * (Decimal(1) - self.tax_interest_rate)
        return annual_rate

    def calculate_periods_per_investment(self):
        # Calculate the total number of periods between interests [n]
        if 0 >= self.compounding_per_year >= 366:
            raise ValueError("compounding_per_year must be grater than 0 and lower than 366")
        periods_per_investment = self.years * self.compounding_per_year
        return periods_per_investment

    def calculate_periodic_interest_rate(self):
        # Convert to the periodic_interest_rate [i]
        if self.interest_type == InterestType.NOMINAL:
            # nominal annual rate (APR)
            periodic_interest_rate = self.calculate_annual_interest_rate() / Decimal(self.compounding_per_year)
            return periodic_interest_rate
        elif self.interest_type == InterestType.EFFECTIVE:
            # effective annual rate (EAR)
            periodic_interest_rate = ((Decimal(1) + self.calculate_annual_interest_rate()) ** (Decimal(1) / Decimal(self.compounding_per_year))) - Decimal(1)
            return periodic_interest_rate
        else:
            # invalid input
            raise ValueError("interest_type must be 'nominal' (APR) or 'effective' (EAR)")

    def with_years(self, years: int):
        return InvestmentContext(
            years=years,
            annual_interest_rate=self.annual_interest_rate,
            compounding_per_year=self.compounding_per_year,
            interest_type=self.interest_type,
            ter_fee=self.ter_fee,
            tax_interest_rate=self.tax_interest_rate,
        )


class Deposit:
    # Zvážit rozdělení Deposit na Deposit(ABC),EntryDeposit(Deposit) a PeriodicDeposit(Deposit)
    def __init__(
        self,
        deposit_type: DepositType,
        amount: int,
        deposits_per_year: int,
        fee_amount: int,
        fee_type: FeeType = FeeType.PROPORTIONAL,
        annuity_type: AnnuityType = AnnuityType.DUE,
    ):
        self.deposit_type = deposit_type
        self.amount = Decimal(amount)
        self.deposits_per_year = deposits_per_year    # applied only for periodic deposits
        self.annuity_type = annuity_type
        self.fee_amount = Decimal(fee_amount)
        self.fee_type = fee_type
        self.fee = self.calculate_real_fee()

    def calculate_total_deposit_amount(self, context: InvestmentContext):
        if self.deposit_type == DepositType.ENTRY:
            return self.amount
        elif self.deposit_type == DepositType.PERIODIC:
            return self.amount * self.deposits_per_year * context.years
        else:
            raise ValueError("deposit_type must be 'entry' or 'periodic'")

    def calculate_real_fee(self):
        if self.fee_type == FeeType.PROPORTIONAL:
            fee = Decimal(self.amount) * Decimal(self.fee_amount)
            return fee
        elif self.fee_type == FeeType.FIXED:
            fee = Decimal(self.fee_amount)
            return fee
        else:
            raise ValueError("fee_type must be 'proportional' or 'exact'")

    def calculate_future_value(self, context: InvestmentContext):
        if self.deposit_type == DepositType.ENTRY:
            future_value = (self.amount - self.fee) * ((Decimal(1) + context.calculate_periodic_interest_rate()) ** context.calculate_periods_per_investment())
            return future_value

        elif self.deposit_type == DepositType.PERIODIC:
            if self.deposits_per_year <= 0:
                raise ValueError("for deposit_type == 'periodic' value of deposits_per_year must be greater than 0")
            elif self.deposits_per_year == context.compounding_per_year:
                # classic formula for future value - faster calculation than time simulation
                future_value_annuity = (self.amount - self.fee) * ((((Decimal(1) + context.calculate_periodic_interest_rate()) ** (Decimal(self.deposits_per_year) * Decimal(context.years))) - 1) / context.calculate_periodic_interest_rate())
                if self.annuity_type == AnnuityType.DUE:
                    future_value_annuity *= (Decimal(1) + context.calculate_periodic_interest_rate())
                return future_value_annuity
            else:
                # time simulation
                total_days = context.years * 365

                if context.interest_type == InterestType.NOMINAL:
                    daily_rate = context.calculate_annual_interest_rate() / Decimal(365)
                else:
                    daily_rate = (Decimal(1) + context.calculate_annual_interest_rate()) ** (Decimal(1) / Decimal(365)) - Decimal(1)

                deposit_interval = Decimal(365) / Decimal(self.deposits_per_year)
                future_value_annuity = Decimal("0")

                for k in range(context.years * self.deposits_per_year):
                    deposit_day = int(k * deposit_interval)
                    remaining_days = total_days - deposit_day
                    future_value_annuity += self.amount * ((Decimal(1) + daily_rate) ** remaining_days)

                return future_value_annuity

        else:
            # invalid input
            raise ValueError("deposit_type must be 'entry' or 'periodic'")
