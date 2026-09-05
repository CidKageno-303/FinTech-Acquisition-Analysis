import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

df =  pd. read_csv('fintech_users.csv')

#   Q1: Which channel has the highest 90-day retention rate?
retention = df.groupby('acquisition_channel')['retained'].mean() * 100
retention = retention.sort_values(ascending=False)
print("90-day Retention Rate by Channel:")
print(retention.round(2))

#   Q2: Which channel has the lowest activation gap?
activation = df.groupby('acquisition_channel')['first_transaction_date'].apply(lambda x: x.notna().mean()) * 100
activation = activation.sort_values(ascending=False)
print("\nActivation Rate by Channel(% who made the first transaction):")
print(activation.round(2))

#   Q3: LTV-to-CAC ratio by channel
cac_ltv = df.groupby('acquisition_channel').agg(
    avg_cac=('cac_usd', 'mean'),
    avg_ltv=('ltv_90_usd', 'mean'),
).reset_index()
cac_ltv['ltv_to_cac_ratio'] = cac_ltv['avg_ltv'] / cac_ltv['avg_cac']
cac_ltv = cac_ltv.sort_values('ltv_to_cac_ratio', ascending=False)
print("\nLTV-to-CAC Ratio by Channel:")
print(cac_ltv.round(2))



# ——— Visualizations ———

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.patch.set_facecolor('#0d0d0d')

colors = ['#00C49F', '#FF6B6B', '#FFD93D', '#6C63FF']
channels = retention.index.tolist()

# Chart 1 - Channel-wise 90-day Retention Rate
axes[0].bar(channels, retention, color=colors)
axes[0].set_facecolor('#1a1a1a')
axes[0].set_title('90-Day Retention Rate (%)', color='white', fontsize=13)
axes[0].tick_params(colors='white')
axes[0].set_xticklabels(channels, rotation=15, ha='right')

# Chart 2 - Channel-wise Activation 
axes[1].bar(activation.index, activation.values, color=colors)
axes[1].set_facecolor('#1a1a1a')
axes[1].set_title('Activation Rate (%)', color='white', fontsize=13)
axes[1].tick_params(colors='white')
axes[1].set_xticklabels(activation.index, rotation=15, ha='right')

# Chart 3 - LTV-to-CAC Ratio by Channel
axes[2].bar(cac_ltv['acquisition_channel'], cac_ltv['ltv_to_cac_ratio'], color=colors)
axes[2].set_facecolor('#1a1a1a')
axes[2].set_title('LTV-to-CAC Ratio', color='white', fontsize=13)
axes[2].tick_params(colors='white')
axes[2].set_xticklabels(cac_ltv['acquisition_channel'], rotation=15, ha='right')

plt.suptitle('FinTech User Acquisition Analysis', color='white', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('fintech_acquisition.png', dpi=150, bbox_inches='tight', facecolor='#0d0d0d')
plt.show()

print("\nCharts saved as fintech_acquisition.png")