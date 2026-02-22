from decimal import Decimal


class InvestmentContext:

    def __init__(
        self,
        years: int,
        annual_interest_rate: Decimal,
        compounding_per_year: int,
        interest_type: str,
        ter_fee: Decimal,
    ):
        self.years = years
        self.annual_interest_rate = annual_interest_rate
        self.compounding_per_year = compounding_per_year # Míra kapitalizace úroku max. 365x ročně = každý den; min 1x ročně
        self.interest_type = interest_type # Is this an effective annual rate or a nominal annual rate compounded m-times per year? Effective annual (EAR) = "effective", Compounded nominal annual rate (APR) = "nominal".
        self.ter_fee = ter_fee

    def calculate_annual_interest_rate(self):
        # Apply TER on annual level
        if self.ter_fee > 0:
            annual_interest_rate = (Decimal(1) + self.annual_interest_rate) * (Decimal(1) - self.ter_fee) - Decimal(1)
        return annual_interest_rate

    def calculate_periodic_interest_rate(self, compounding_per_year: int, interest_type: str):
        """
        Calculate periodic interest rate adjusted for TER [i].
        :return: periodic_interest_rate, number_of_periods
        """
        # Calculate the total number of periods between interests [n]
        if 0 >= compounding_per_year >= 365:
            raise ValueError("compounding_per_year must be grater than 0 and lower than 366")

        # Convert to the periodic_interest_rate [i]
        if interest_type == "nominal":
            # nominal annual rate (APR)
            periodic_interest_rate = self.calculate_annual_interest_rate() / Decimal(compounding_per_year)
            return periodic_interest_rate
        elif interest_type == "effective":
            # effective annual rate (EAR)
            periodic_interest_rate = ((Decimal(1) + self.calculate_annual_interest_rate()) ** (
                        Decimal(1) / Decimal(compounding_per_year))) - Decimal(1)
            return periodic_interest_rate
        else:
            # invalid input
            raise ValueError("interest_type must be 'nominal' (APR) or 'effective' (EAR).")


class Deposit:
    """
    deposit_type: str    # "entry" or "periodic"
    amount: Decimal
    fee: Decimal
    if deposit_type == "periodic": deposits_per_year: int
    annuity_type: str    # "ordinary" or "due"
    """

    def __init__(self, deposit_type, amount, deposits_per_year, annuity_type, fee):
        self.deposit_type = deposit_type
        self.amount = amount
        self.deposits_per_year = deposits_per_year    # applied only for periodic deposits
        self.annuity_type = annuity_type
        self.fee = fee

    def calculate_future_value(self, context: InvestmentContext):
        if self.deposit_type == "entry":
            future_value = (self.amount - self.fee) * ((Decimal(1) + context.calculate_annual_interest_rate()) ** context.years)
            return future_value
        elif self.deposit_type == "periodic":
            if self.deposits_per_year <= 0:
                raise ValueError("for deposit_type == 'periodic' value of deposits_per_year must be greater than 0")
            if self.deposits_per_year == context.compounding_per_year:
                # klasický vzorec pro FV
                future_value_annuity = (self.amount - self.fee) * ((((Decimal(1) + context.calculate_periodic_interest_rate()) ** (self.deposits_per_year * context.years)) - 1) / context.calculate_periodic_interest_rate())
                if self.annuity_type == "due":
                    future_value_annuity *= (Decimal(1) + context.calculate_periodic_interest_rate())
                return future_value_annuity
            else:
                # časová simulace
                pass
        else:
            # invalid input
            raise ValueError("deposit_type must be 'entry' or 'periodic'")

    def apply_annual_inflation(self, inflation_rate):

        pass
