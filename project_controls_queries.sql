-- ==================================================================================
-- CAPITAL PROJECT CONTROLS & EARNED VALUE MANAGEMENT (EVM) SQL SUITE
-- Dataset: Capital Project Management & Milestone Tracking Records (2,500 Deliverables)
-- ==================================================================================

-- 1. Discipline-Level Earned Value Performance Summary
SELECT 
    discipline,
    COUNT(*) AS total_deliverables,
    ROUND(SUM(planned_value_usd)::numeric, 2) AS total_planned_budget,
    ROUND(SUM(earned_value_usd)::numeric, 2) AS total_earned_value,
    ROUND(SUM(actual_cost_usd)::numeric, 2) AS total_actual_cost,
    -- Cost Performance Index (CPI = EV / AC)
    ROUND((SUM(earned_value_usd) / NULLIF(SUM(actual_cost_usd), 0))::numeric, 3) AS cpi,
    -- Cost Variance (CV = EV - AC)
    ROUND((SUM(earned_value_usd) - SUM(actual_cost_usd))::numeric, 2) AS cost_variance_usd,
    -- Overall Discipline Completion %
    ROUND((SUM(earned_value_usd) / NULLIF(SUM(planned_value_usd), 0) * 100)::numeric, 1) AS discipline_progress_pct
FROM capital_project_tasks
GROUP BY discipline
ORDER BY total_planned_budget DESC;


-- 2. Top Critical-Path Delays & High-Risk Deliverables
-- Filters deliverables with schedule delay > 25% and CPI < 0.90
SELECT 
    deliverable_id,
    discipline,
    project_phase,
    planned_duration_days,
    actual_duration_days,
    (actual_duration_days - planned_duration_days) AS schedule_delay_days,
    ROUND((earned_value_usd / NULLIF(actual_cost_usd, 0))::numeric, 3) AS cpi,
    completion_pct,
    CASE 
        WHEN (actual_duration_days - planned_duration_days) > 20 AND (earned_value_usd / NULLIF(actual_cost_usd, 0)) < 0.90 THEN 'RED: Critical Cost & Schedule Delay'
        WHEN (actual_duration_days - planned_duration_days) > 10 THEN 'YELLOW: Schedule Slippage Alert'
        ELSE 'GREEN: Manageable Variance'
    END AS risk_tier
FROM capital_project_tasks
WHERE (actual_duration_days - planned_duration_days) > 15
ORDER BY schedule_delay_days DESC
LIMIT 15;
