'''
A - control (so original design)
B - variant (new design)
'''
import pandas as pd 
import numpy as np 
from scipy.stats import chi2_contingency
# Simulation data for A and B groups 
np.random.seed(42)
group = ['A'] * 1000 + ['B'] * 1000
conversions = np.random.choice([0, 1], size=2000, p=[0.9, 0.1])
data = pd.DataFrame({'Group': group, 'Conversion': conversions})

print(data.head())

# Analysis
conversion_rates = data.groupby('Group')['Conversion'].mean()
print(conversion_rates)

# Statistical Test (Chi-Square Test)
contingency_table = pd.crosstab(data['Group'], data['Conversion'])
chi2, p, _, _ = chi2_contingency(contingency_table)

print(f"Chi-Square Statistic: {chi2}, p-value: {p}")
if p < 0.05:
    print("Statistically significant difference!")
else:
    print("No significant difference.")
