CREATE INDEX IF NOT EXISTS bom_source_material_idx
ON bom_source (plant_id, year, produced_material)
