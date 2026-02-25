from decimal import Decimal

# Deposits
years = int(20)
annual_interest_rate = Decimal(0.05)
entry_deposit = Decimal(5000.00)

periodic_deposit = Decimal(1000.00)
deposits_per_year = int(12)
# type_interest_periodic_deposits_calculation = str("intermediate") # Is this an effective annual rate or a nominal annual rate compounded m-times per year? Annual (EAR) = "annual", Compounded (APR) = "intermediate".
interest_type = str("nominal") # Is this an effective annual rate or a nominal annual rate compounded m-times per year? Effective annual (EAR) = "effective", Compounded nominal annual rate (APR) = "nominal".
annuity_type = str("due") # "due" = deposit at beginning of period; "ordinary" = deposit at the end of period
# interest_on_last_deposit = True # Is the last deposit also interest-bearing? (i.e. the number of interest-bearing deposits is the same as the number of deposits = the final 'total amount' reached is calculated just before the next deposit).

# Not implemented yet:
"""additional_contribution_exists = False
if additional_contribution_exists:
    additional_contribution = Decimal(300.00)
    additional_contribution_per_year = int(4)
    type_interest_contribution_calculation = str("annual")
    interest_on_last_contribution = True # Is the last additional contribution also interest-bearing? ...same as above."""


# Fees
entry_fee_proportional_to_amount = True
if entry_fee_proportional_to_amount:
    entry_fee = entry_deposit * Decimal(0.0015)
else:
    entry_fee = Decimal(0.00)

every_deposit_fee_proportional_to_amount = True
if every_deposit_fee_proportional_to_amount:
    every_deposit_fee = periodic_deposit * Decimal(0.0015)
else:
    every_deposit_fee = Decimal(30.00)

ter_fee = Decimal(0.0003) # TER = Total Expense Ratio [% of total assets]
management_fee = Decimal(0.00) # Management fee [per year] when don't know exact TER value.


# Calculator logic

# Calculate the total number of deposits (= number_of_periods [n])
if deposits_per_year <= 0:
    raise ValueError("deposits_per_year must be greater than 0")
number_of_periods = deposits_per_year * years

# Apply TER on annual level
if ter_fee > 0:
    annual_interest_rate = (Decimal(1) + annual_interest_rate) * (Decimal(1) - ter_fee) - Decimal(1)

# Add inflation here?

# Convert to the periodic_interest_rate [i]
if interest_type == "nominal":
    # nominal annual rate (APR)
    periodic_interest_rate = annual_interest_rate / deposits_per_year
elif interest_type == "effective":
    # effective annual rate (EAR)
    periodic_interest_rate = (
        (Decimal(1) + annual_interest_rate)
        ** (Decimal(1) / Decimal(deposits_per_year))
    ) - Decimal(1)
else:
    # invalid input
    raise ValueError(
        "interest_type must be 'nominal' (APR) or 'effective' (EAR)."
    )


# Calculate the total amount of deposits with entry deposit
total_deposits_amount = entry_deposit + periodic_deposit * number_of_periods

# Calculate the total amount achieved over years of saving/investing
future_value_from_entry = (entry_deposit - entry_fee) * (1 + periodic_interest_rate) ** number_of_periods

total_amount_from_periodic_deposits = (periodic_deposit - every_deposit_fee) * (((1 + periodic_interest_rate) ** number_of_periods) - 1) / periodic_interest_rate
if annuity_type == "due":
    total_amount_from_periodic_deposits = (periodic_deposit - every_deposit_fee) * (((1 + periodic_interest_rate) ** number_of_periods) - 1) / periodic_interest_rate * (1 + periodic_interest_rate)

total_management_fee = management_fee * (1 + (periodic_interest_rate * deposits_per_year)) ** years / (periodic_deposit * deposits_per_year)

total_amount = future_value_from_entry + total_amount_from_periodic_deposits - total_management_fee



withdrawal_fee_proportional_to_amount = False
if withdrawal_fee_proportional_to_amount:
    withdrawal_fee = total_amount * Decimal(0.01)
else:
    withdrawal_fee = Decimal(0.00)


# Print the total amount of deposits with entry deposit
print(f'Celkový vložený obnos {total_deposits_amount} CZK')
# Print the total amount achieved over years of saving/investing
print(f'Celková naspořená částka {total_amount} CZK')
print(f'FV za vstupní vklad: {future_value_from_entry}'
      f'\nFV za periodický vklad {total_amount_from_periodic_deposits}')