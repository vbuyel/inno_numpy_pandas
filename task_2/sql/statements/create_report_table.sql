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
)
