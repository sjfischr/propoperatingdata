import faker
import pandas as pd
import random

# Initialize Faker
generator = faker.Faker()

# Define the categories for income and expenses
income_categories = [
    "Gross Potential Rent",
    "Vacancy",
    "Concessions",
    "Bad Debt",
    "Laundry Income",
    "Parking Income",
    "Utility Reimbursement",
    "Other Income",
    "Commercial Income",
    "Commercial Vacancy"
]
expense_categories = [
    "Real Estate Taxes",
    "Other Taxes",
    "Insurance",
    "Fuel / Gas",
    "Electricity",
    "Trash Removal",
    "Water and Sewer",
    "Bldg Maint and Repair",
    "Cleaning/Turnover",
    "Gardening and Landscape",
    "Management Fee",
    "Office Salary",
    "Maintenance Salary",
    "Security Salary",
    "Payroll Taxes & Benefits",
    "Apt. Allowance",
    "Marketing",
    "Professional Fees",
    "Office Expenses",
    "Miscellaneous Expenses"
]

# Generate random T12 data
def generate_t12_data():
    data = []
    for month_offset in range(12):
        month = pd.Timestamp.now() - pd.DateOffset(months=month_offset)
        monthly_data = {
            "Month": month.strftime("%B %Y"),
            "Gross Potential Rent": random.randint(25000, 35000),
            "Vacancy": -random.randint(1000, 5000),
            "Concessions": -random.randint(500, 2000),
            "Bad Debt": -random.randint(500, 1500),
            "Laundry Income": random.randint(500, 1000),
            "Parking Income": random.randint(300, 800),
            "Utility Reimbursement": random.randint(700, 1500),
            "Other Income": random.randint(1000, 3000),
            "Commercial Income": random.randint(2000, 5000),
            "Commercial Vacancy": -random.randint(500, 2000),
            "Real Estate Taxes": random.randint(3000, 5000),
            "Other Taxes": random.randint(500, 1500),
            "Insurance": random.randint(800, 1500),
            "Fuel / Gas": random.randint(500, 1000),
            "Electricity": random.randint(1000, 3000),
            "Trash Removal": random.randint(300, 700),
            "Water and Sewer": random.randint(1000, 2000),
            "Bldg Maint and Repair": random.randint(1000, 3000),
            "Cleaning/Turnover": random.randint(500, 1500),
            "Gardening and Landscape": random.randint(300, 800),
            "Management Fee": random.randint(1500, 2500),
            "Office Salary": random.randint(2000, 4000),
            "Maintenance Salary": random.randint(1500, 3000),
            "Security Salary": random.randint(1000, 2000),
            "Payroll Taxes & Benefits": random.randint(800, 1500),
            "Apt. Allowance": random.randint(300, 700),
            "Marketing": random.randint(500, 1500),
            "Professional Fees": random.randint(500, 1000),
            "Office Expenses": random.randint(300, 800),
            "Miscellaneous Expenses": random.randint(200, 600),
        }
        data.append(monthly_data)
    return data

# Generate the T12 DataFrame
def generate_t12_dataframe(building_name, address):
    t12_data = generate_t12_data()
    t12_df = pd.DataFrame(t12_data)

    # Add building information
    t12_df.insert(0, "Building Name", building_name)
    t12_df.insert(1, "Address", address)

    # Calculate Net Operating Income (NOI)
    t12_df["Total Income"] = t12_df[income_categories].sum(axis=1)
    t12_df["Total Expenses"] = t12_df[expense_categories].sum(axis=1)
    t12_df["Net Operating Income (NOI)"] = t12_df["Total Income"] - t12_df["Total Expenses"]

    return t12_df

# Generate a T12 statement for a single building and save as Excel
def generate_single_t12_excel():
    building_name = generator.company() + " Apartments"
    address = generator.address()
    t12_df = generate_t12_dataframe(building_name, address)

    # Create a new DataFrame to structure the output more like a traditional P&L statement
    output_data = []
    output_data.append(["Building Name", building_name])
    output_data.append(["Address", address])
    output_data.append([])  # Empty row for spacing
    output_data.append(["Month"] + t12_df["Month"].tolist())  # Adding Month row
    output_data.append([])  # Empty row for spacing
    output_data.append(["Income"])  # Income header

    for category in income_categories:
        output_data.append([category] + t12_df[category].tolist())

    output_data.append([])  # Empty row for spacing
    output_data.append(["Expenses"])  # Expenses header

    for category in expense_categories:
        output_data.append([category] + t12_df[category].tolist())

    output_data.append([])  # Empty row for spacing
    output_data.append(["Total Income"] + t12_df["Total Income"].tolist())
    output_data.append(["Total Expenses"] + t12_df["Total Expenses"].tolist())
    output_data.append(["Net Operating Income (NOI)"] + t12_df["Net Operating Income (NOI)"].tolist())

    # Convert the structured output data to a DataFrame
    formatted_df = pd.DataFrame(output_data)

    # Save to Excel with formatting improvements
    output_filename = "T12_Financial_Statement_{}.xlsx".format(building_name.replace(" ", "_"))
    with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
        formatted_df.to_excel(writer, index=False, header=False, sheet_name="T12 Statement")

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets["T12 Statement"]

        # Apply formatting to headers and titles for better readability
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'align': 'center',
            'border': 1
        })

        # Format the first few rows as headers
        for row_num in range(4):
            worksheet.set_row(row_num, cell_format=header_format)

        # Set column width for better readability
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:Z', 15)

    print(f"Generated T12 Financial Statement for '{building_name}' and saved to '{output_filename}'")

# Generate a single T12 Excel file
generate_single_t12_excel()
