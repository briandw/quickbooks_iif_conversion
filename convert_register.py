import csv
import datetime


def csv_to_qif(input_csv: str, output_qif: str):
    """
    Converts a CSV file to a QIF file for import into GnuCash.

    :param input_csv: Path to the input CSV file.
    :param output_qif: Path to the output QIF file.
    """
    # Open the input CSV git standard output QIF files
    with open(input_csv, 'r', encoding='utf-8') as csv_file, open(output_qif, 'w', encoding='utf-8') as qif_file:
        reader = csv.reader(csv_file, delimiter='\t')

        title = None
        # Skip non-header rows until the real headers are found
        for row in reader:
            if isinstance(row, list) and len(row) == 1:
                title = row[0]
                continue

            if "Date" in row:
                headers = row  # Extract headers for DictReader
                break

        # Create a DictReader with the extracted headers
        csv_file.seek(0)
        reader = csv.DictReader(csv_file, fieldnames=headers, delimiter='\t')

        # Write QIF header for bank account transactions
        qif_file.write("!Type:Bank\n")

        for row in reader:

            if row['Date'] == title or row['Date'] == 'Date':
                continue  # Skip the actual header row in the file
            
            # Parse the necessary fields
            date = row['Date']
            payee = row.get('Name', '').strip()
            memo = row.get('Memo', '').strip()
            amount = row.get('Amount', '').strip()
            reconciled = row.get('C', '').strip()
            transfer_account = row.get('Account', '').strip()

            # Convert date to QIF format (MM/DD/YY)
            try:
                parsed_date = datetime.datetime.strptime(date, '%m/%d/%y')
                formatted_date = parsed_date.strftime('%m/%d/%Y')
            except ValueError as e:
                print(f"Invalid date format in row: {row} {e}")
                assert False

            # Write the transaction to the QIF file
            qif_file.write(f"D{formatted_date}\n")  # Date
            qif_file.write(f"T{amount}\n")          # Amount
            if payee:
                qif_file.write(f"P{payee}\n")       # Payee/Description
            if memo:
                qif_file.write(f"M{memo}\n")       # Memo
            if transfer_account:
                qif_file.write(f"L{transfer_account}\n")  # Transfer Account
            if reconciled:
                qif_file.write("C*\n")             # Cleared status

            # End of transaction
            qif_file.write("^\n")

if __name__ == "__main__":
    # Input CSV file path
    input_csv = "qb_register.csv"  # Replace with the path to your CSV file

    # Output QIF file path
    output_qif = "register.qif"  # Replace with the desired QIF file path

    # Convert the CSV to QIF
    csv_to_qif(input_csv, output_qif)
    print(f"QIF file successfully created at {output_qif}")
