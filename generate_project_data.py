import pandas as pd
import numpy as np

np.random.seed(42)
n = 2500

disciplines = ['Piping & Layout', 'Civil & Structural', 'Mechanical Equipment', 'Electrical', 'Instrumentation & Control']
phases = ['Engineering & Design', 'Procurement & Fabrication', 'Construction & Erection', 'Pre-Commissioning']

disc_col = np.random.choice(disciplines, size=n, p=[0.35, 0.20, 0.15, 0.15, 0.15])
phase_col = np.random.choice(phases, size=n, p=[0.30, 0.25, 0.35, 0.10])

# Budget at Completion (BAC in USD) per task
planned_value_usd = np.random.lognormal(mean=8.5, sigma=0.8, size=n) # ~$1,000 to $45,000 per deliverable/spool

# Progress % (0 to 100)
progress_pct = np.random.beta(a=2, b=1.5, size=n) * 100
earned_value_usd = planned_value_usd * (progress_pct / 100.0)

# Actual Cost (AC): some tasks under budget, some over budget
cost_factor = np.random.normal(1.04, 0.15, size=n) # avg 4% cost overrun
cost_factor = np.clip(cost_factor, 0.70, 1.60)
actual_cost_usd = earned_value_usd * cost_factor

# Schedule variance: planned vs actual days
planned_days = np.random.randint(15, 120, size=n)
schedule_factor = np.random.normal(1.06, 0.20, size=n) # avg 6% schedule delay
actual_days = np.round(planned_days * schedule_factor)

df = pd.DataFrame({
    'deliverable_id': [f"DEL-{i+10001}" for i in range(n)],
    'discipline': disc_col,
    'project_phase': phase_col,
    'planned_value_usd': np.round(planned_value_usd, 2),
    'earned_value_usd': np.round(earned_value_usd, 2),
    'actual_cost_usd': np.round(actual_cost_usd, 2),
    'completion_pct': np.round(progress_pct, 1),
    'planned_duration_days': planned_days,
    'actual_duration_days': actual_days.astype(int)
})

df.to_csv('/home/user/capital_project_controls/data/capital_project_evm_data.csv', index=False)
print(f"Generated {len(df)} project controls records in capital_project_controls/data/")
