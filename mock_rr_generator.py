# Script to Generate Rent Roll Spreadsheet using Faker

from faker import Faker
import pandas as pd
import random

# Initialize Faker instance
fake = Faker()

# Define the number of units to generate
num_units = int(input("Enter the number of units: "))

# Input parameters
building_name = input("Enter the Building Name: ")
property_management_company = input("Enter the Property Management Company Name: ")
gross_potential_rent = float(input("Enter the Gross Potential Rent (GPR): "))

# Generate header information
general_info = {
    "Rent Roll As Of Date": fake.date_between_dates(date_start=pd.Timestamp('2024-01-01'), date_end=pd.Timestamp('2024-10-31')),
    "Property Name": building_name,
    "Property Street Address": fake.street_address(),
    "Property City": fake.city(),
    "Property State": fake.state_abbr(),
    "Property Zip Code": fake.zipcode(),
    "Property Management Company Name": property_management_company,
    "Submitter Email Address": fake.email(),
    "Seller Loan Number": fake.bothify(text='??###########')
}

# Define average rent values based on unit type
average_rent_by_unit_type = {
    "S": 1464,
    "1": 1791,
    "2": 2276,
    "3": 3248
}

# Generate rent roll data using Faker with constraints
rent_roll_data = {
    "Unit Identifier": [fake.unique.random_int(min=1, max=100) for _ in range(num_units)],
    "Unit Bedrooms Count": [fake.random_int(min=0, max=3) for _ in range(num_units)],
    "Unit Full Bathrooms Count": [fake.random_int(min=1, max=2) for _ in range(num_units)],
    "Unit Half Bathrooms Count": [fake.random_int(min=0, max=1) for _ in range(num_units)],
    "Unit Square Feet Number": [fake.random_int(min=500, max=1500) for _ in range(num_units)],
    "Unit/Tenant Lease Status Type": [None for _ in range(num_units)],
    "Market Comparable Rent Amount": [],
    "Tenant Contract Rent Amount": [],
    "Subsidy Type": [None for _ in range(num_units)],
    "Other Subsidy Description": [None for _ in range(num_units)],
    "Subsidy Detailed Amount": [],
    "Security Deposit Amount": [round(random.uniform(500, 1500), 2) for _ in range(num_units)],
}

# Generate tenant contract rent ensuring total does not exceed GPR
total_rent = 0
for i in range(num_units):
    unit_type = ["S", "1", "2", "3"][rent_roll_data["Unit Bedrooms Count"][i]]
    average_rent = average_rent_by_unit_type[unit_type]
    remaining_rent_allowance = max(gross_potential_rent - total_rent, 0)
    max_rent = min(average_rent * 1.1, remaining_rent_allowance) if remaining_rent_allowance > 0 else 0
    tenant_rent = round(random.uniform(average_rent * 0.9, max_rent), 2) if max_rent > 0 else 0
    rent_roll_data["Tenant Contract Rent Amount"].append(tenant_rent)
    total_rent += tenant_rent

    # Market Comparable Rent Amount should be in line with Tenant Contract Rent Amount
    market_rent = round(tenant_rent * random.uniform(0.95, 1.1), 2)
    rent_roll_data["Market Comparable Rent Amount"].append(market_rent)

    # Subsidy Detailed Amount - randomly generate subsidy if applicable
    rent_roll_data["Subsidy Detailed Amount"].append(
        round(random.uniform(0, 500), 2) if random.random() < 0.3 else None
    )

# Create DataFrame for rent roll data
rent_roll_df = pd.DataFrame(rent_roll_data)

# Create a DataFrame for the general information (header)
general_info_df = pd.DataFrame([general_info])

# Save to Excel file with both general information and rent roll data
output_file = f"rent_roll_generated_{building_name.replace(' ', '_')}.xlsx"
with pd.ExcelWriter(output_file) as writer:
    general_info_df.to_excel(writer, sheet_name="General Info", index=False)
    rent_roll_df.to_excel(writer, sheet_name="Rent Roll", index=False)

print(f"Rent roll spreadsheet generated and saved to {output_file}")


