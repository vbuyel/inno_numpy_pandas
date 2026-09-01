CREATE VIEW bom_annual AS
SELECT
    plant_id,
    -- Keeping year while omitting month combines monthly rows into a calendar year.
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
    plant_id,
    year,
    produced_material,
    produced_material_production_type,
    produced_material_release_type,
    component_material,
    component_material_production_type,
    component_material_release_type
