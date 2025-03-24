import csv
import time

def verify_csv(filepath="../data/220720COVID19MEXICO.csv"):
    start_time = time.time()
    wrong_values = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Get the header row
            expected_columns = len(header)
            print(f"Expected columns: {expected_columns}")

            bad_row_count = 0
            row_count = 1  # Start from 1, after the header.
            bad_value_count = 0
            for row in reader:
                row_count += 1
                if len(row) != expected_columns:
                    bad_row_count += 1
                    # print(f"Warning: Row {row_count} has {len(row)} columns (expected {expected_columns}).")
                    # Optionally, print the row: print(row)
                else:
                    if len(row) >= 17: #added check here.
                        try:
                            value = int(row[16])  # Column 17 (index 16)
                            if value not in (1, 2, 99):
                                wrong_values.append((row_count, row))
                                bad_value_count += 1
                        except ValueError:
                            wrong_values.append((row_count, row))
                            bad_value_count += 1
                    else:
                        wrong_values.append((row_count, row))
                        bad_value_count += 1

            print(f"Total rows: {row_count}")
            print(f"Rows with incorrect column count: {bad_row_count}")
            print(f"Rows with incorrect value count: {bad_value_count}")

            for row_num, wrong_value in wrong_values:
                print(f"Row {row_num}: {wrong_value}")

    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds")

verify_csv()