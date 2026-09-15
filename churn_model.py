import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns

# —— Load Data ——
df = pd.read_csv('fintech_users.csv')

# —— Feature Engineering ——
df['activated'] = df['first_transaction_date'].notna().astype(int)

features = ['activated', 
            'tx_frequency_30d',
            'tx_frequency_60',
            'tx_frequency_90',
            'cac_usd',
            'ltv_90_usd'
            ]

# Encode acquisition channel
df['channel_encoded'] = df['acquisition_channel'].astype('category').cat.codes

x = df[features]
y = df['churned'].astype(int)

# —— Split Data ——
X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# —— Train Model ——
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# —— Evaluate Model —— 
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Retained', 'Churned']))

# —— Feature Importance —— 
importance = pd.DataFrame({
    'feature': features,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\nFeature Importance:")
print(importance)

# —— Visualization ——
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('#0d0d0d')

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Retained', 'Churned'],
            yticklabels=['Retained', 'Churned'],
            ax=axes[0])
axes[0].set_facecolor('#1a1a1a')
axes[0].set_title('Confusion Matrix', color='white', fontsize=13)
axes[0].tick_params(colors='white')
axes[0].yaxis.label.set_color('white')
axes[0].xaxis.label.set_color('white')

# Feature Importance
axes[1].barh(importance['feature'], importance['importance'], color='#00C49F')
axes[1].set_facecolor('#1a1a1a')
axes[1].set_title('Feature Importance', color='white', fontsize=13)
axes[1].tick_params(colors='white')

plt.suptitle('Churn Prediction Model — Random Forest', color='white', 
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('Churn_model.png', dpi=150, bbox_inches='tight',
            facecolor='#0d0d0d')
plt.show()

print("\nChart saved as churn_model.png")
