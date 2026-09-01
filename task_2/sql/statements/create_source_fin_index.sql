CREATE INDEX IF NOT EXISTS bom_source_fin_idx
ON bom_source (produced_material_release_type, plant_id, year)
