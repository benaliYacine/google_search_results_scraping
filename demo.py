import pandas as pd

# Load the files
file_A = pd.read_excel("A.xlsx")
file_B = pd.read_excel("B.xlsx")

# Step 2: Remove completely empty columns from file B
file_C = file_B.dropna(axis=1, how='all')

# Step 3A: Enrich file C with matching records from file A
if 'domain' not in file_C.columns:
    file_C['domain'] = None

for i in range(1, 6):  # Add up to 5 columns for emails
    email_column = f'email_{i}'
    if email_column not in file_C.columns:
        file_C[email_column] = None

for index, row in file_A.iterrows():
    matching_rows = file_C[file_C['Dossiernummer'] == row['KVK nummer']]
    if not matching_rows.empty:
        for _, match_row in matching_rows.iterrows():
            file_C.at[match_row.name, 'domain'] = row['Bedrijfsnaam']
            emails = str(row['e-mail algemeen']).split(';')
            for i, email in enumerate(emails):
                if i < 5:
                    file_C.at[match_row.name, f'email_{i+1}'] = email.strip()

# Step 3B: Add non-matching records from file A to file C
new_rows = []
for index, row in file_A.iterrows():
    matching_rows = file_C[file_C['Dossiernummer'] == row['KVK nummer']]
    if matching_rows.empty:
        new_row = {
            'Dossiernummer': row['KVK nummer'],
            'Handelsnaam DM': row['Bedrijfsnaam'],
            'Telefoon-netnummer': row['Straatnaam'],
            'Straatnaam vestigingsadres': row['Straatnaam'],
            'Toevoeging huisnummer vestigingsadres': row['Huisnummer toevoeging'],
            'Postkode vestigingsadres': row['Postcode'],
            'Woonplaats vestigingsadres': row['Plaats'],
            'domain': row['Bedrijfsnaam'],
            'color': 'yellow'
        }
        emails = str(row['e-mail algemeen']).split(';')
        for i, email in enumerate(emails):
            if i < 5:
                new_row[f'email_{i+1}'] = email.strip()
        new_rows.append(new_row)
for new_row in new_rows:
    file_C = file_C.append(new_row, ignore_index=True)

# Save the enriched file
file_C.to_excel("enriched_file.xlsx", index=False)
