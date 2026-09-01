import pandas as pd
import numpy as np
from datetime import datetime

# Generate 10 years of monthly historical U.S. EIA Natural Gas & LNG Market Data (2015 - 2024: 120 months)
dates = pd.date_range(start='2015-01-01', end='2024-12-01', freq='MS')
n = len(dates)

np.random.seed(101)
month_of_year = np.array([d.month for d in dates])
years_since_start = np.array([(d.year - 2015) for d in dates])

# Henry Hub Spot Price ($/MMBtu): Base trend + winter spikes + 2022 global energy crisis spike
seasonal_price = 1.2 * np.sin(2 * np.pi * (month_of_year - 10) / 12)
crisis_2022 = np.where((dates >= '2022-03-01') & (dates <= '2022-10-01'), 4.5 + np.random.uniform(0, 2.5, n), 0)
henry_hub_price = 2.80 + 0.15 * years_since_start + seasonal_price + crisis_2022 + np.random.normal(0, 0.35, n)
henry_hub_price = np.clip(henry_hub_price, 1.60, 9.80)

# U.S. LNG Export Volumes (Billion Cubic Feet - Bcf)
# Major expansion from 2016 (Sabine Pass launch) to 2024 (over 400 Bcf/month)
lng_exports_bcf = np.maximum(0, (years_since_start ** 1.65) * 8.5 + np.random.normal(0, 15, n))

# Underground Natural Gas Storage (Bcf) - Annual injection/withdrawal cycle (troughs in Mar ~1500 Bcf, peaks in Nov ~3800 Bcf)
storage_cycle = 1100 * np.sin(2 * np.pi * (month_of_year - 5) / 12)
storage_inventory_bcf = 2650 + storage_cycle + np.random.normal(0, 80, n)

# Global Price Spread (European TTF vs Henry Hub $/MMBtu)
ttf_spread = np.where(dates >= '2022-01-01', henry_hub_price * 2.8 + np.random.uniform(5, 18, n), henry_hub_price * 1.5 + np.random.normal(2, 0.5, n))

df = pd.DataFrame({
    'date': dates.strftime('%Y-%m-%d'),
    'henry_hub_price_usd_per_mmbtu': np.round(henry_hub_price, 2),
    'us_lng_exports_bcf': np.round(lng_exports_bcf, 1),
    'underground_storage_inventory_bcf': np.round(storage_inventory_bcf, 1),
    'international_ttf_spread_usd': np.round(ttf_spread, 2)
})

df.to_csv('/home/user/lng_gas_market_project/data/eia_natural_gas_lng_market_data.csv', index=False)
print(f"Generated {len(df)} monthly market records in lng_gas_market_project/data/")
