CREATE VIEW bom_explosion AS
WITH RECURSIVE roots AS (
    SELECT DISTINCT
        plant_id AS plant,
        year AS fin_year,
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
        r.plant, r.fin_year, r.fin_material_id, r.fin_material_release_type,
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
     AND b.year = r.fin_year
     AND b.produced_material = r.first_material_id
    WHERE r.first_material_release_type IN ('FIN', 'PROD')

    UNION ALL

    SELECT
        h.plant, h.fin_year, h.fin_material_id, h.fin_material_release_type,
        h.fin_material_production_type, h.fin_production_quantity,
        b.produced_material, b.produced_material_release_type,
        b.produced_material_production_type, b.produced_material_quantity,
        b.component_material, b.component_material_release_type,
        b.component_material_production_type, b.component_material_quantity,
        h.path || b.produced_material
    FROM hierarchy h
    JOIN bom_annual b
      ON b.plant_id = h.plant
     AND b.year = h.fin_year
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
    fin_year AS year
FROM hierarchy
