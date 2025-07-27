

import pandas as pd
from fpdf import FPDF
from datetime import datetime

# ---------------------------
# 1. Load the Dataset
# ---------------------------
df = pd.read_csv("uber.csv")  # Make sure uber.csv is in the same directory
print("✅ Dataset loaded successfully")

# ---------------------------
# 2. Data Understanding & Cleaning
# ---------------------------

# a. Inspect data shape
print("Initial dataset shape:", df.shape)

# b. Check for missing values
print("Missing values per column:\n", df.isnull().sum())

# c. Drop rows with any missing values
df.dropna(inplace=True)
print("Shape after dropping missing values:", df.shape)

# d. Convert 'pickup_datetime' to datetime format
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

# ---------------------------
# 3. Exploratory Data Analysis (EDA)
# ---------------------------

# Descriptive statistics
desc = df.describe()
print("Descriptive statistics:\n", desc)

# Additional statistics
print("Median fare_amount:", df['fare_amount'].median())
print("Mode fare_amount:", df['fare_amount'].mode()[0])
print("Standard deviation:", df['fare_amount'].std())

# Quartiles and data range
print("Fare Amount Quartiles:\n", df['fare_amount'].quantile([0.25, 0.5, 0.75]))
print("Fare Amount Range:", df['fare_amount'].min(), "to", df['fare_amount'].max())

# ---------------------------
# 4. Feature Engineering
# ---------------------------

# Extract time features
df['hour'] = df['pickup_datetime'].dt.hour
df['day'] = df['pickup_datetime'].dt.day
df['month'] = df['pickup_datetime'].dt.month
df['day_of_week'] = df['pickup_datetime'].dt.day_name()

# Optional: Add peak/off-peak indicator
def label_peak(hour):
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        return "Peak"
    else:
        return "Off-Peak"

df['peak_time'] = df['hour'].apply(label_peak)

# Remove fare outliers (extremely low or high fares)
df = df[(df['fare_amount'] > 0) & (df['fare_amount'] < 200)]

# Save cleaned and enhanced data
df.to_csv("cleaned_uber_fares.csv", index=False)
print("✅ Cleaned and enhanced dataset saved as 'cleaned_uber_fares.csv'")

# ---------------------------
# 5. PDF Documentation
# ---------------------------

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Uber Fares Dashboard (.pbix) - Full Project Description", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", '', 12)
content = [
    "This document describes the structure and purpose of the Uber_Fares_Dashboard.pbix file created as part of the Uber Fares Data Analysis project.",
    "",
    "PBIX File Contents:",
    "1. Dataset: Cleaned and transformed data exported from Python after data wrangling.",
    "2. Data Model:",
    "   * Relationships established between variables (e.g., date-time, fare amount)",
    "   * Time-based features engineered: Hour, Day of Week, Month, Peak Time",
    "",
    "-" * 50,
    "",
    "Power BI Visuals Included:",
    "* Histogram of Fare Amounts",
    "* Boxplot for Fare Outliers",
    "* Bar chart: Number of rides by Hour of Day",
    "* Line chart: Average fare by Day of Week",
    "* Donut chart: Total fare by Month",
    "* Map visual (if coordinates available) for spatial trends",
    "",
    "-" * 50,
    "",
    "Dashboard Features:",
    "* Interactive slicers for filtering by date and time",
    "* Tooltips for detailed ride metrics",
    "* Clean and consistent formatting",
    "",
    "-" * 50,
    "",
    "Insights Delivered:",
    "* Identification of peak hours for Uber rides",
    "* Common fare ranges and outliers",
    "* Time-based trends in ride frequency and fare pricing",
    "",
    "-" * 50,
    "",
    "Tools Used:",
    "* Python (Pandas, Matplotlib) for data cleaning and EDA",
    "* Power BI for dashboard design and visualization",
    "",
    "-" * 50,
    "",
    "PBIX File Link:",
    "Download the .pbix file here: https://drive.google.com/file/d/1df0aOG7HO7kNrDoYEsnBjGl8NfVxvvT2/view?usp=drivesdk",
    "",
    f"Generated on: {datetime.now().strftime('%d %B %Y')}"
]

for line in content:
    pdf.multi_cell(0, 10, txt=line)

pdf.output("Uber_Fares_Dashboard_pbix_Description_WITH_LINK.pdf")
print("✅ PDF report saved as 'Uber_Fares_Dashboard_pbix_Description_WITH_LINK.pdf'")
