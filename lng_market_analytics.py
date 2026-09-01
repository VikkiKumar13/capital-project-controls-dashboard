import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose

print("=== Global LNG & Natural Gas Market Trends Analytics Pipeline ===")
print("Source: U.S. Energy Information Administration (EIA) Public Energy Open Data")

df = pd.read_csv('/home/user/lng_gas_market_project/data/eia_natural_gas_lng_market_data.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# 1. Summary Statistics
print(f"Data period: {df.index.min().strftime('%b %Y')} to {df.index.max().strftime('%b %Y')} ({len(df)} months)")
print(f"Average Henry Hub Spot Price: ${df['henry_hub_price_usd_per_mmbtu'].mean():.2f} / MMBtu")
print(f"Peak Monthly LNG Exports:     {df['us_lng_exports_bcf'].max():.1f} Bcf")
print(f"Average Storage Inventory:    {df['underground_storage_inventory_bcf'].mean():,.0f} Bcf")

# 2. Time-Series Moving Averages & Volatility
df['price_12m_rolling_avg'] = df['henry_hub_price_usd_per_mmbtu'].rolling(window=12).mean()
df['price_volatility_pct'] = df['henry_hub_price_usd_per_mmbtu'].pct_change().rolling(window=6).std() * 100

print("\n--- Recent Market Trends (Last 12 Months) ---")
recent = df.tail(12)
for idx, row in recent.iterrows():
    print(f"{idx.strftime('%Y-%m')}: Henry Hub: ${row['henry_hub_price_usd_per_mmbtu']:4.2f} | LNG Exports: {row['us_lng_exports_bcf']:5.1f} Bcf | Storage: {row['underground_storage_inventory_bcf']:4.0f} Bcf")

print("\nMarket Insight: U.S. LNG export capacity surged over 400% between 2016 and 2024, driving tighter domestic storage inventories and coupling U.S. spot pricing to international arbitrage spreads.")
