import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Set the style for the plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 10)
plt.rcParams['font.size'] = 12

# Define allocation scenarios
allocations = [0.01, 0.05, 0.10]  # 1%, 5%, 10% BTC allocation
scenarios = ['Bear Market', 'Base Case', 'Bull Market']
colors = ['#FF9999', '#66B2FF', '#99CC99']

# Define expected returns and volatilities for different market scenarios
expected_returns = {
    'Bear Market': {'BTC': -0.20, 'Traditional': 0.02},
    'Base Case': {'BTC': 0.30, 'Traditional': 0.06},
    'Bull Market': {'BTC': 0.80, 'Traditional': 0.10}
}

volatilities = {
    'Bear Market': {'BTC': 0.80, 'Traditional': 0.15},
    'Base Case': {'BTC': 0.65, 'Traditional': 0.12},
    'Bull Market': {'BTC': 0.70, 'Traditional': 0.14}
}

# Generate portfolio returns for each scenario and allocation
results = {}
num_simulations = 1000
time_horizon = 5  # years

for scenario in scenarios:
    scenario_results = {}
    
    # Traditional portfolio (0% BTC)
    trad_returns = np.random.normal(
        expected_returns[scenario]['Traditional'], 
        volatilities[scenario]['Traditional'], 
        (num_simulations, time_horizon)
    )
    trad_cumulative = np.cumprod(1 + trad_returns, axis=1)
    scenario_results[0] = trad_cumulative
    
    # Portfolios with BTC allocation
    for alloc in allocations:
        # Blend returns based on allocation
        btc_weight = alloc
        trad_weight = 1 - alloc
        
        blended_returns = np.zeros((num_simulations, time_horizon))
        for i in range(num_simulations):
            btc_sim_returns = np.random.normal(
                expected_returns[scenario]['BTC'], 
                volatilities[scenario]['BTC'], 
                time_horizon
            )
            trad_sim_returns = np.random.normal(
                expected_returns[scenario]['Traditional'], 
                volatilities[scenario]['Traditional'], 
                time_horizon
            )
            
            # Combine returns based on allocation weights
            blended_returns[i] = btc_weight * btc_sim_returns + trad_weight * trad_sim_returns
        
        # Calculate cumulative returns
        cumulative_returns = np.cumprod(1 + blended_returns, axis=1)
        scenario_results[alloc] = cumulative_returns
    
    results[scenario] = scenario_results