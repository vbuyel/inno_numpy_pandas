DROP VIEW IF EXISTS bom_explosion;
DROP VIEW IF EXISTS bom_annual;

CREATE TABLE IF NOT EXISTS bom_source (
    year integer NOT NULL,
    month integer NOT NULL CHECK (month BETWEEN 1 AND 12),
    produced_material text NOT NULL,
    produced_material_production_type integer NOT NULL,
    produced_material_release_type text NOT NULL,
    produced_material_quantity numeric NOT NULL,
    component_material text NOT NULL,
    component_material_production_type integer,
    component_material_release_type text NOT NULL,
    component_material_quantity numeric NOT NULL,
    plant_id text NOT NULL
);

CREATE INDEX IF NOT EXISTS bom_source_material_idx
    ON bom_source (plant_id, year, produced_material);
CREATE INDEX IF NOT EXISTS bom_source_fin_idx
    ON bom_source (produced_material_release_type, plant_id, year);

CREATE TABLE IF NOT EXISTS bom_report (
    plant text NOT NULL,
    fin_material_id text NOT NULL,
    fin_material_release_type text NOT NULL,
    fin_material_production_type integer NOT NULL,
    fin_production_quantity numeric NOT NULL,
    prod_material_id text NOT NULL,
    prod_material_release_type text NOT NULL,
    prod_material_production_type integer NOT NULL,
    prod_material_production_quantity numeric NOT NULL,
    component_id text NOT NULL,
    component_material_release_type text NOT NULL,
    component_material_production_type integer,
    component_consumption_quantity numeric NOT NULL,
    year integer NOT NULL
);

CREATE INDEX IF NOT EXISTS bom_report_lookup_idx
    ON bom_report (plant, year, fin_material_id);

CREATE VIEW bom_annual AS
SELECT
    plant_id,
    year,
    produced_material,
    produced_material_production_type,
    produced_material_release_type,
    component_material,
    component_material_production_type,
    component_material_release_type,
    SUM(produced_material_quantity) AS produced_material_quantity,
    SUM(component_material_quantity) AS component_material_quantity
FROM bom_source
GROUP BY
    plant_id, year, produced_material, produced_material_production_type,
    produced_material_release_type, component_material,
    component_material_production_type, component_material_release_type;

CREATE VIEW bom_explosion AS
WITH RECURSIVE roots AS (
    SELECT DISTINCT
        plant_id AS plant,
        year,
        produced_material AS fin_material_id,
        produced_material_release_type AS fin_material_release_type,
        produced_material_production_type AS fin_material_production_type,
        produced_material_quantity AS fin_production_quantity,
        component_material AS first_material_id,
        component_material_release_type AS first_material_release_type
    FROM bom_annual
    WHERE produced_material_release_type = 'FIN'
),
hierarchy AS (
    SELECT
        r.plant, r.year, r.fin_material_id, r.fin_material_release_type,
        r.fin_material_production_type, r.fin_production_quantity,
        b.produced_material AS prod_material_id,
        b.produced_material_release_type AS prod_material_release_type,
        b.produced_material_production_type AS prod_material_production_type,
        b.produced_material_quantity AS prod_material_production_quantity,
        b.component_material AS component_id,
        b.component_material_release_type,
        b.component_material_production_type,
        b.component_material_quantity AS component_consumption_quantity,
        ARRAY[r.fin_material_id, b.produced_material] AS path
    FROM roots r
    JOIN bom_annual b
      ON b.plant_id = r.plant
     AND b.year = r.year
     AND b.produced_material = r.first_material_id
    WHERE r.first_material_release_type IN ('FIN', 'PROD')

    UNION ALL

    SELECT
        h.plant, h.year, h.fin_material_id, h.fin_material_release_type,
        h.fin_material_production_type, h.fin_production_quantity,
        b.produced_material, b.produced_material_release_type,
        b.produced_material_production_type, b.produced_material_quantity,
        b.component_material, b.component_material_release_type,
        b.component_material_production_type, b.component_material_quantity,
        h.path || b.produced_material
    FROM hierarchy h
    JOIN bom_annual b
      ON b.plant_id = h.plant
     AND b.year = h.year
     AND b.produced_material = h.component_id
    WHERE h.component_material_release_type IN ('FIN', 'PROD')
      AND NOT b.produced_material = ANY(h.path)
)
SELECT DISTINCT
    plant,
    fin_material_id,
    fin_material_release_type,
    fin_material_production_type,
    fin_production_quantity,
    prod_material_id,
    prod_material_release_type,
    prod_material_production_type,
    prod_material_production_quantity,
    component_id,
    component_material_release_type,
    component_material_production_type,
    component_consumption_quantity,
    year
FROM hierarchy;
