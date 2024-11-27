# Property Opertaing Data Synthesizer
This is a collection of files and code which synthesizes property operating data such as T12s and Rent Rolls. This data is completely synthetic.

There are two components to the solution: the Rent Roll Spreadsheet Generator, and the T12 Financial Statement Generator

## Rent Roll Spreadsheet Generator
This Python script generates a detailed rent roll spreadsheet using the Faker library for creating realistic synthetic data. It allows you to enter the building name, property management company, and gross potential rent (GPR). The script produces a rent roll, ensuring that:

Tenant Contract Rent Amount is correlated with unit type (e.g., Studio, 1BR, 2BR, 3BR) while staying within the Gross Potential Rent limit.
Market Comparable Rent Amount is aligned with the Tenant Contract Rent Amount.
Generates the Rent Roll As Of Date for the year 2024.
The resulting Excel file includes:

- General Info - Property information such as name, address, management company, and loan number.
- Rent Roll - Detailed information for each unit, including rent, amenities, subsidy, and security deposit details.
- This script is perfect for testing data workflows, generating sample data, or automating synthetic data creation for rental properties.

## T12 Financial Statement Generator
This project generates Trailing Twelve Month (T12) financial statements for real estate properties using Python. The T12 tool helps generate realistic financial summaries including income and expense categories over the past twelve months for multifamily properties. The key features include:

- Ability to generate synthetic T12 data for multiple properties.
- Categories for income and expenses to align with standard T12 formats used in commercial real estate.
- Utilizes Faker for creating realistic data and provides a structure suitable for data analysis, visualization, or integration into property management systems.
- This script is ideal for simulating real estate financial analysis workflows, building machine learning datasets, or demonstrating financial statement processing for multifamily properties.
