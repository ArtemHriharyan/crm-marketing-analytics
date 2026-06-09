-- =========================================================
-- Data cleaning script for Yandex Metrica tables
-- Project: CRM Marketing Analytics
-- Purpose:
-- 1. Standardize traffic source names
-- 2. Group minor/unknown sources into "Other"
-- 3. Add visit duration in minutes
-- =========================================================

-- Standardize source_engine values in goals table

UPDATE fact_metrica_goals
SET source_engine =
    CASE
        WHEN source_engine NOT IN (
            'Yandex',
            'Google',
            'Ad traffic',
            'Direct traffic'
        )
        THEN 'Other'
        ELSE source_engine
    END;

-- Standardize source_engine values in main traffic table

UPDATE fact_metrica_main
SET source_engine =
    CASE
        WHEN source_engine IS NULL THEN traffic_source
        WHEN source_engine LIKE 'Yandex, search results' THEN 'Yandex'
        WHEN source_engine LIKE 'Google, search results' THEN 'Google'
        WHEN source_engine LIKE 'Yandex Mobile' THEN 'Yandex'
        WHEN source_engine LIKE 'Google: mobile app' THEN 'Google'
        ELSE source_engine
    END;

-- Add average visit duration column

ALTER TABLE fact_metrica_main_1
ADD COLUMN IF NOT EXISTS avg_visit_duration_min NUMERIC;

-- Calculate average visit duration in minutes

UPDATE fact_metrica_main_1
SET avg_visit_duration_min =
    ROUND((avg_visit_duration_sec / 60.0)::numeric, 2);