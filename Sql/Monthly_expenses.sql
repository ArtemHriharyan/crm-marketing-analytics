-- DROP TABLE IF EXISTS public.monthly_expenses;

CREATE TABLE IF NOT EXISTS public.monthly_expenses
(
    expense_month date NOT NULL,
    seo_promotion numeric(12,2) NOT NULL,
    ads_management numeric(12,2) NOT NULL,
    priority_mgmt numeric(12,2) NOT NULL,
    priority_budget numeric(12,2) NOT NULL,
    CONSTRAINT monthly_expenses_pkey PRIMARY KEY (expense_month)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.monthly_expenses
    OWNER to postgres;