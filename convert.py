
import csv
import datetime
from typing import Optional
from iif_data_types import *

def parse_iif_file(file_path: str) -> dict[RowType, list]:
    data: dict[RowType, list] = {row_type: [] for row_type in RowType}
    current_section: Optional[RowType] = None
    headers: list[str] = []

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.rstrip('\n')
            if not line:
                continue  # Skip empty lines

            if line.startswith('!'):
                # New section header with field names
                current_section_str = line[1:]
                # Use csv.reader to split the line
                reader = csv.reader([current_section_str], delimiter='\t', quoting=csv.QUOTE_NONE)
                headers = next(reader)
                line_type = headers[0]
                current_section = RowType.__members__.get(line_type)
                if current_section is None:
                    print(f"Warning: Unknown section '{line_type}' at line {line_num}")
            elif current_section:
                # Use csv.reader to split the line
                reader = csv.reader([line], delimiter='\t', quoting=csv.QUOTE_NONE)
                values = next(reader)
                assert len(headers) >= len(values)-1, f"Header and value count mismatch: {headers} {values}"

                record_dict = dict(zip(headers, values))

                # Route to the appropriate class using match
                match current_section:
                    case RowType.HDR:
                        hdr = HDR.from_row(record_dict)
                        data[RowType.HDR].append(hdr)
                    case RowType.ACCNT:
                        account = Account.from_row(record_dict)
                        data[RowType.ACCNT].append(account)
                    case RowType.INVITEM:
                        invitem = InventoryItem.from_row(record_dict)
                        data[RowType.INVITEM].append(invitem)
                    case RowType.CLASS:
                        class_record = ClassRecord.from_row(record_dict)
                        data[RowType.CLASS].append(class_record)
                    case RowType.VTYPE:
                        vtype = VendorType.from_row(record_dict)
                        data[RowType.VTYPE].append(vtype)
                    case RowType.EMP:
                        employee = Employee.from_row(record_dict)
                        data[RowType.EMP].append(employee)
                    case RowType.BUD:
                        budget = Budget.from_row(record_dict)
                        data[RowType.BUD].append(budget)
                    case RowType.TODO:
                        todo_item = ToDoItem.from_row(record_dict)
                        data[RowType.TODO].append(todo_item)
                    case RowType.VEHICLE:
                        vehicle = Vehicle.from_row(record_dict)
                        data[RowType.VEHICLE].append(vehicle)
                    case RowType.SALESREP:
                        sales_rep = SalesRep.from_row(record_dict)
                        data[RowType.SALESREP].append(sales_rep)
                    case RowType.CTYPE:
                        ctype = CustomerType.from_row(record_dict)
                        data[RowType.CTYPE].append(ctype)
                    case RowType.CUST:
                        customer = Customer.from_row(record_dict)
                        data[RowType.CUST].append(customer)
                    case RowType.VEND:
                        vendor = Vendor.from_row(record_dict)
                        data[RowType.VEND].append(vendor)
                    case RowType.SHIPMETH:
                        ship_meth = ShippingMethod.from_row(record_dict)
                        data[RowType.SHIPMETH].append(ship_meth)
                    case RowType.PAYMETH:
                        pay_meth = PaymentMethod.from_row(record_dict)
                        data[RowType.PAYMETH].append(pay_meth)
                    case RowType.TERMS:
                        terms = Terms.from_row(record_dict)
                        data[RowType.TERMS].append(terms)
                    case RowType.SALESTAXCODE:
                        stc = SalesTaxCode.from_row(record_dict)
                        data[RowType.SALESTAXCODE].append(stc)
                    case RowType.ENDGRP:
                        current_section = None  # End of group
                    case RowType.OTHERNAME:
                        othername = OtherName.from_row(record_dict)
                        data[RowType.OTHERNAME].append(othername)
                        
                    case _:
                        assert False, f"Unknown row type: {current_section}"
            else:
                assert False, f"No current section: {line}"

    return data


def export_to_iif(data: dict[RowType, list], output_file: str):
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        for row_type in RowType:
            records = data.get(row_type, [])

            # Get the class corresponding to the row type
            record_class = get_class_by_row_type(row_type)
            if not record_class:
                assert False, f"Unknown row type: {row_type}"

            # Write the section header with field names, starting with '!'
            header_fields = record_class.to_iif_header()
            f.write(header_fields + '\n')

            # Write the data lines
            for record in records:
                f.write(record.to_iif_row() + '\n')

def map_account_type(account_type: str) -> str:
    """Maps custom account types to GnuCash-compatible QIF account types."""
    mapping = {
        'EXEXP': 'Oth A',     # Other Asset for Expenses
        'EXINC': 'Oth A',     # Other Asset for Income
        'EXP': 'Oth A',       # Other Asset for Expenses
        'INC': 'Oth A',       # Other Asset for Income
        'EQUITY': 'Oth A',    # Other Asset for Equity
        'LTLIAB': 'Oth L',    # Other Liability for Long-Term Liabilities
        'OCLIAB': 'Oth L',    # Other Liability for Other Current Liabilities
        'FIXASSET': 'Oth A',  # Other Asset for Fixed Assets
        'OCASSET': 'Oth A',   # Other Asset for Other Current Assets
    }
    return mapping.get(account_type, 'Bank')  # Default to Bank if not mapped


def export_to_qif(data: dict[RowType, list], output_file: str):
    with open(output_file, 'w', encoding='utf-8') as f:
        accounts = data.get(RowType.ACCNT, [])
        for account in accounts:
            # Map the account type to GnuCash-compatible type
            account_type = map_account_type(account.ACCNTTYPE)
            
            # Write the account header
            f.write("!Account\n")
            f.write(f"N{account.NAME}\n")
            f.write(f"T{account_type}\n")
            if account.DESC:
                f.write(f"D{account.DESC}\n")
            f.write("^\n")

            # Start a new section for transactions (empty if no transactions)
            f.write(f"!Type:{account_type.lower()}\n")

            # Include opening balance as a transaction if necessary
            if account.OBAMOUNT:
                f.write(f"D{datetime.datetime.now().strftime('%m/%d/%Y')}\n")
                f.write(f"T{account.OBAMOUNT}\n")
                f.write("C*\n")  # Cleared status
                f.write("MOpening Balance\n")
                f.write("^\n")


def export_vendors_to_csv(data: dict[RowType, list], output_file: str):
    import csv

    vendors = data.get(RowType.VEND, [])
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'ID', 'Company', 'Name', 'Address1', 'Address2', 'Address3', 'Address4',
            'Phone', 'Fax', 'Email', 'Notes', 'Shipping Name', 'Shipping Address1',
            'Shipping Address2', 'Shipping Address3', 'Shipping Address4',
            'Shipping Phone', 'Shipping Fax', 'Shipping Email'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for idx, vendor in enumerate(vendors, start=1):
            writer.writerow({
                'ID': idx,
                'Company': vendor.COMPANYNAME or '',
                'Name': vendor.NAME,
                'Address1': vendor.ADDR1 or '',
                'Address2': vendor.ADDR2 or '',
                'Address3': vendor.ADDR3 or '',
                'Address4': vendor.ADDR4 or '',
                'Phone': vendor.PHONE1 or '',
                'Fax': vendor.FAXNUM or '',
                'Email': vendor.EMAIL or '',
                'Notes': vendor.NOTEPAD or '',
                'Shipping Name': '',
                'Shipping Address1': '',
                'Shipping Address2': '',
                'Shipping Address3': '',
                'Shipping Address4': '',
                'Shipping Phone': '',
                'Shipping Fax': '',
                'Shipping Email': ''
            })

def export_othernames_to_csv(data: dict[RowType, list], output_file: str):
    import csv

    other_names = data.get(RowType.OTHERNAME, [])
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'ID', 'Company', 'Name', 'Address1', 'Address2', 'Address3', 'Address4',
            'Phone', 'Fax', 'Email', 'Notes', 'Shipping Name', 'Shipping Address1',
            'Shipping Address2', 'Shipping Address3', 'Shipping Address4',
            'Shipping Phone', 'Shipping Fax', 'Shipping Email'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for idx, othername in enumerate(other_names, start=1):
            writer.writerow({
                'ID': idx,
                'Company': othername.COMPANYNAME or '',
                'Name': othername.NAME,
                'Address1': othername.BADDR1 or '',
                'Address2': othername.BADDR2 or '',
                'Address3': othername.BADDR3 or '',
                'Address4': othername.BADDR4 or '',
                'Phone': othername.PHONE1 or '',
                'Fax': othername.FAXNUM or '',
                'Email': othername.EMAIL or '',
                'Notes': othername.NOTEPAD or '',
                'Shipping Name': '',
                'Shipping Address1': '',
                'Shipping Address2': '',
                'Shipping Address3': '',
                'Shipping Address4': '',
                'Shipping Phone': '',
                'Shipping Fax': '',
                'Shipping Email': ''
            })


def export_customers_to_csv(data: dict[RowType, list], output_file: str):

    customers = data.get(RowType.CUST, [])
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Phone', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for customer in customers:
            writer.writerow({
                'Name': customer.NAME,
                'Address': f"{customer.BADDR1 or ''} {customer.BADDR2 or ''} {customer.BADDR3 or ''} {customer.BADDR4 or ''} {customer.BADDR5 or ''}",
                'Phone': customer.PHONE1 or '',
                'Email': customer.EMAIL or '',
            })



def csv_to_qif(input_csv: str, output_qif: str):
    """
    Converts a CSV file to a QIF file for import into GnuCash.

    :param input_csv: Path to the input CSV file.
    :param output_qif: Path to the output QIF file.
    """
    # Open the input CSV and output QIF files
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
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert IIF file to various formats')
    parser.add_argument('input_file', help='Input IIF file path')
    parser.add_argument('--qif', help='Export to QIF file', metavar='FILE')
    parser.add_argument('--customers', help='Export customers to CSV file', metavar='FILE') 
    parser.add_argument('--vendors', help='Export vendors to CSV file', metavar='FILE')
    parser.add_argument('--othernames', help='Export other names to CSV file', metavar='FILE')
    
    args = parser.parse_args()

    data = parse_iif_file(args.input_file)
    
    # Print summary
    for k, v in data.items():
        print(f"{k}: {len(v)}")
    print(f"{len(data)} categories")
    num_records = sum(len(records) for records in data.values())
    print(f"{num_records} records")

    if args.qif:
        export_to_qif(data, args.qif)
    if args.customers:
        export_customers_to_csv(data, args.customers)
    if args.othernames:
        export_othernames_to_csv(data, args.othernames)
    if args.vendors:
        export_vendors_to_csv(data, args.vendors)

