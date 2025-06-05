import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Define custody models and their attributes
custody_models = [
    'Self-Custody (Cold Storage)',
    'Qualified Custodian',
    'Exchange Custody',
    'Multi-Signature Solution'
]

# Define attributes for comparison
attributes = [
    'Security Level',
    'Cost',
    'Access Speed',
    'Regulatory Compliance',
    'Insurance Coverage',
    'Operational Complexity'
]

# Create sample data for the comparison table
# Values range from 1 (lowest/worst) to 5 (highest/best)
data = {
    'Self-Custody (Cold Storage)': [5, 5, 2, 3, 1, 2],
    'Qualified Custodian': [4, 2, 3, 5, 5, 4],
    'Exchange Custody': [2, 4, 5, 3, 3, 5],
    'Multi-Signature Solution': [4, 3, 3, 4, 3, 3]
}

# Create DataFrame
df = pd.DataFrame(data, index=attributes)

# Optional: visualize as heatmap
plt.figure(figsize=(10,6))
sns.heatmap(df, annot=True, cmap='YlGnBu', cbar=False)
plt.title("Bitcoin Custody Model Comparison")
plt.show()