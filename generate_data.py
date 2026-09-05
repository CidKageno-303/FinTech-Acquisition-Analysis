import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n_users = 10000

channels = ['Paid Ads', 'Referrals', 'Organic Search', 'Social Media']
channel_weights = [0.35, 0.25, 0.20, 0.20]

retention_rates = {
    'Paid Ads': 0.35,
    'Referrals': 0.72,
    'Organic Search': 0.58,
    'Social Media': 0.28
}

activation_rates = {
    'Paid Ads': 0.40,
    'Referrals': 0.78,
    'Organic Search': 0.62,
    'Social Media': 0.32
}

cac = {
    'Paid Ads': 12,
    'Referrals': 4,
    'Organic Search': 6,
    'Social Media': 8
}

avg_transaction_value = {
    'Paid Ads': 45,
    'Referrals': 95,
    'Organic Search': 70,
    'Social Media': 38
}

rows = []
start_date = datetime(2025, 1, 1)

for user_id in range(1, n_users + 1):
    channel = str(np.random.choice(channels, p=channel_weights))
    signup_date = start_date + timedelta(days=np.random.randint(0, 180))

    activated = np.random.random() < activation_rates[channel]

    if activated:
        days_to_first = np.random.randint(1, 15)
        first_transaction_date = signup_date + timedelta(days=days_to_first)
    else:
        first_transaction_date = None

    retained = np.random.random() < retention_rates[channel]
    churned = not retained

    if activated and retained:
        tx_30 = np.random.randint(1, 8)
        tx_60 = tx_30 + np.random.randint(1, 8)
        tx_90 = tx_60 + np.random.randint(1, 8)
    elif activated and not retained:
        tx_30 = np.random.randint(1, 4)
        tx_60 = tx_30 + np.random.randint(0, 2)
        tx_90 = tx_60
    else:
        tx_30 = tx_60 = tx_90 = 0

    avg_val = avg_transaction_value[channel]
    ltv_90 = round(tx_90 * np.random.normal(avg_val, avg_val * 0.2), 2)
    ltv_90 = max(0, ltv_90)

    rows.append({
        'user_id': user_id,
        'acquisition_channel':channel,
        'signup_date': signup_date.strftime('%Y-%m-%d'),
        'first_transaction_date': first_transaction_date.strftime('%Y-%m-%d') if first_transaction_date else None,
        'churned': churned,
        'retained': retained,
        'tx_frequency_30d': tx_30,
        'tx_frequency_60': tx_60,
        'tx_frequency_90': tx_90,
        'cac_usd': cac[channel],
        'ltv_90_usd': ltv_90
    })

df = pd.DataFrame(rows)
df.to_csv('fintech_users.csv', index=False)

print(f"Dataset generated: {len(df)} users")
print(f"\nChannel distribution:")
print(df['acquisition_channel'].value_counts())
print(f"\nSample data:")
print(df.head())