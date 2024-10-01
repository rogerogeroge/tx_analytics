import json
from collections import defaultdict
from datetime import datetime

# Exchange rate for converting stars to dollars
STARS_TO_USD_RATE = 1981 / 152347  # Approximate rate

# Function to load data from file
def load_transactions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('transactions', [])

# Function to convert stars to dollars
def convert_stars_to_usd(stars):
    return stars * STARS_TO_USD_RATE

# Function to process transactions only for the Notcoin partner
def process_transactions_for_notcoin(transactions):
    notcoin_stats = defaultdict(lambda: defaultdict(int))

    for transaction in transactions:
        # Extract invoice_payload
        invoice_payload = transaction.get('source', {}).get('invoice_payload', 'deguard')

        # Check if this is a transaction for the Notcoin partner
        if invoice_payload == 'not_coin_integration':
            amount_stars = transaction['amount']
            date = datetime.fromtimestamp(transaction['date'])
            month = date.strftime('%Y-%m')  # Format: YYYY-MM

            # Determine the type of plan
            if 200 <= amount_stars <= 350:
                plan = '1_month'
            elif 1500 <= amount_stars <= 2100:
                plan = '12_month'
            elif 4500 <= amount_stars <= 7500:
                plan = 'lifetime'
            else:
                plan = 'other'

            # Aggregation of data by months
            notcoin_stats[month]['total_stars'] += amount_stars
            notcoin_stats[month][plan] += 1

    return notcoin_stats

# Partner's revenue share
REV_SHARE = 0.40  # Profit share for the partner

# Function to print statistics for the Notcoin partner
def print_stats_for_notcoin(notcoin_stats):
    total_stars_all = 0
    total_usd_all = 0

    print(f"<b>Notcoin stats</b>")

    for month, month_stats in notcoin_stats.items():
        total_stars = month_stats['total_stars']
        total_usd = convert_stars_to_usd(total_stars)
        total_stars_all += total_stars
        total_usd_all += total_usd
        partner_profit = total_usd * REV_SHARE  # Net profit for the partner
        total_usd_all_x_rev = total_usd_all * REV_SHARE

        print(f"\n{month}:")
        print(f"  Profit - <b>{total_stars} stars, {total_usd:.2f} USD</b>")
        print(f"  Partner's net profit - <b>{partner_profit:.2f} USD</b>")

        if month_stats.get('1_month', 0) > 0:
            print(f"    1-month plans - {month_stats['1_month']} items")
        if month_stats.get('12_month', 0) > 0:
            print(f"    Annual plans - {month_stats['12_month']} items")
        if month_stats.get('lifetime', 0) > 0:
            print(f"    Lifetime passes - {month_stats['lifetime']} items")

    print(f"\n<br><br>Total Notcoin profit for all time - <b>{total_stars_all} stars, {total_usd_all:.2f} USD</b>")
    print(f"\nRevShare Notcoin profit for all time - <b>{total_usd_all_x_rev:.2f} USD</b>")
    print(f"\n% RevShare - <b>{REV_SHARE*100}%</b>")

# Main function
def main():
    file_path = 'response.json'  # Specify the path to your transactions file
    transactions = load_transactions(file_path)
    notcoin_stats = process_transactions_for_notcoin(transactions)
    print_stats_for_notcoin(notcoin_stats)

if __name__ == "__main__":
    main()
