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
)
