import pandas as pd
import mysql.connector

# ✅ Load CSV file
df = pd.read_csv(r"C:\Users\LENOVO\Downloads\aws_services.csv")

# ✅ Strip column names (remove leading/trailing spaces)
df.columns = df.columns.str.strip()

# ✅ Remove rows where all fields are empty
df = df.dropna(how='all')

# ✅ Preview first 5 rows
print("📋 Excel Preview (first 5 rows):")
print(df.head())

# ✅ Show all column names
print("\n📋 Columns in CSV:", df.columns.tolist())

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gayathri@123",    # Replace with your password
    database="aws_excel"      # Replace with your DB name
)

cursor = conn.cursor()

# ✅ Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS aws_services (
    service VARCHAR(100),
    description TEXT,
    ownership VARCHAR(100),
    status VARCHAR(100),
    estimated_time VARCHAR(100)
)
""")

# ✅ Track skipped rows
skipped_rows = []

# ✅ Insert data into MySQL
for index, row in df.iterrows():
    # Check for any missing values in the required fields
    if (
        pd.isna(row.get('Service')) or str(row['Service']).strip() == '' or
        pd.isna(row.get('Description')) or str(row['Description']).strip() == '' or
        pd.isna(row.get('ownership')) or str(row['ownership']).strip() == '' or
        pd.isna(row.get('Status')) or str(row['Status']).strip() == '' or
        pd.isna(row.get('Estimated Time')) or str(row['Estimated Time']).strip() == ''
    ):
        skipped_rows.append(index + 2)  # +2 for human-readable row number (including header)
        continue

    # ✅ Insert into DB
    cursor.execute("""
        INSERT INTO aws_services (service, description, ownership, status, estimated_time)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row['Service'],
        row['Description'],
        row['ownership'],
        row['Status'],
        row['Estimated Time']
    ))

conn.commit()

# ✅ Show skipped rows info
if skipped_rows:
    print(f"\n⚠️ Skipped {len(skipped_rows)} row(s) due to missing required fields: {skipped_rows}")
else:
    print("\n✅ All rows inserted without skipping.")

# ✅ Finish
print("✅ Excel data inserted successfully into MySQL!")

cursor.close()
conn.close()
