-- DROP TABLE IF EXISTS public.date_con;

CREATE TABLE IF NOT EXISTS public.date_con
(
    date date,
    year numeric,
    month numeric,
    month_name text COLLATE pg_catalog."default",
    month_year text COLLATE pg_catalog."default",
    week numeric,
    day_of_week_num numeric,
    month_start date,
    day_of_week_name text COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.date_con
    OWNER to postgres;