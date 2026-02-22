from decimal import Decimal

# Deposits
years = int(20)
annual_interest_rate = Decimal(0.05)
entry_deposit = Decimal(100000.00)

periodic_deposit = Decimal(1000.00)
deposits_per_year = int(12)
type_interest_periodic_deposits_calculation = str("intermediate") # Is this an effective annual rate or a nominal annual rate compounded m-times per year? Annual (EAR) = "annual", Compounded (APR) = "intermediate".
annuity_type = str("due") # "due" = deposit at beginning of period; "ordinary" = deposit at the end of period
interest_on_last_deposit = True # Is the last deposit also interest-bearing? (i.e. the number of interest-bearing deposits is the same as the number of deposits = the final 'total amount' reached is calculated just before the next deposit).

# Not implemented yet:
"""additional_contribution_exists = False
if additional_contribution_exists:
    additional_contribution = Decimal(300.00)
    additional_contribution_per_year = int(4)
    type_interest_contribution_calculation = str("annual")
    interest_on_last_contribution = True # Is the last additional contribution also interest-bearing? ...same as above."""


# Fees
entry_fee_proportional_to_amount = False
if entry_fee_proportional_to_amount:
    entry_fee = entry_deposit * Decimal(0.01)
else:
    entry_fee = Decimal(0.00)

every_deposit_fee_proportional_to_amount = False
if every_deposit_fee_proportional_to_amount:
    every_deposit_fee = periodic_deposit * Decimal(0.0015)
else:
    every_deposit_fee = Decimal(30.00)

ter_fee = Decimal(0.0003) # TER = Total Expense Ratio [% of total assets]
management_fee = Decimal(0.00) # Management fee [per year] when don't know exact TER value.



# Calculator logic
if deposits_per_year <= 0:
    raise ValueError("deposits_per_year must be greater than 0")
# Apply TER on annual level
if ter_fee > 0:
    annual_interest_rate = (Decimal(1) + annual_interest_rate) * (Decimal(1) - ter_fee) - Decimal(1)

# Convert to periodic rate
if type_interest_periodic_deposits_calculation == "intermediate":
    # nominal annual rate
    periodic_interest_rate = annual_interest_rate / deposits_per_year
elif type_interest_periodic_deposits_calculation == "annual":
    # effective annual rate
    periodic_interest_rate = (
        (Decimal(1) + annual_interest_rate)
        ** (Decimal(1) / Decimal(deposits_per_year))
    ) - Decimal(1)
else:
    # invalid input
    raise ValueError(
        "type_interest_periodic_deposits_calculation must be 'intermediate' or 'annual'"
    )


# Calculate the total number of deposits (= number of periods [n])
number_of_deposits = deposits_per_year * years
# Calculate the interest rate per period [i]
periodic_interest_rate = annual_interest_rate / deposits_per_year
if ter_fee > 0:
    periodic_interest_rate = (annual_interest_rate - ter_fee) / deposits_per_year

# Calculate the total amount of deposits with entry deposit
total_deposits_amount = entry_deposit + periodic_deposit * number_of_deposits

# Calculate the total amount achieved over years of saving/investing
total_amount_from_entry = (entry_deposit - entry_fee) * (1 + periodic_interest_rate) ** number_of_deposits

total_amount_from_periodic_deposits = (periodic_deposit - every_deposit_fee) * (((1 + periodic_interest_rate) ** number_of_deposits) - 1) / periodic_interest_rate
if annuity_type == "due":
    total_amount_from_periodic_deposits = (periodic_deposit - every_deposit_fee) * (((1 + periodic_interest_rate) ** number_of_deposits) - 1) / periodic_interest_rate * (1 + periodic_interest_rate)

total_management_fee = management_fee * (1 + (periodic_interest_rate * deposits_per_year)) ** years / (periodic_deposit * deposits_per_year)

total_amount = total_amount_from_entry + total_amount_from_periodic_deposits - total_management_fee



withdrawal_fee_proportional_to_amount = False
if withdrawal_fee_proportional_to_amount:
    withdrawal_fee = total_amount * Decimal(0.01)
else:
    withdrawal_fee = Decimal(0.00)


# Print the total amount of deposits with entry deposit
print(f'Celkový vložený obnos {total_deposits_amount} CZK')
# Print the total amount achieved over years of saving/investing
print(f'Celková naspořená částka {total_amount} CZK')