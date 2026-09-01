CREATE INDEX IF NOT EXISTS bom_report_lookup_idx
ON bom_report (plant, year, fin_material_id)
