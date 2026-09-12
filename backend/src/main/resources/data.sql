INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'ENERGY', 'Natural Gas', 2.02, 'kg CO2e/kWh', 'DEFRA 2024'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'ENERGY' AND sub_category = 'Natural Gas');

INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'ENERGY', 'Grid Electricity', 0.85, 'kg CO2e/kWh', 'DEFRA 2024'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'ENERGY' AND sub_category = 'Grid Electricity');

INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'ENERGY', 'Coal', 2.93, 'kg CO2e/kg', 'DEFRA 2024'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'ENERGY' AND sub_category = 'Coal');

INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'MATERIAL', 'Steel', 1.8, 'kg CO2e/kg', 'EPA GHG'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'MATERIAL' AND sub_category = 'Steel');

INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'MATERIAL', 'Aluminum', 11.5, 'kg CO2e/kg', 'EPA GHG'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'MATERIAL' AND sub_category = 'Aluminum');

INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'MATERIAL', 'Cement', 0.9, 'kg CO2e/kg', 'EPA GHG'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'MATERIAL' AND sub_category = 'Cement');

INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'WASTE', 'Industrial Waste', 0.45, 'kg CO2e/kg', 'DEFRA 2024'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'WASTE' AND sub_category = 'Industrial Waste');

INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'WASTE', 'Plastic Waste', 2.8, 'kg CO2e/kg', 'DEFRA 2024'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'WASTE' AND sub_category = 'Plastic Waste');

INSERT INTO emission_factor (id, category, sub_category, factor_value, unit, source)
SELECT gen_random_uuid(), 'TRANSPORT', 'Diesel Truck', 2.68, 'kg CO2e/liter', 'DEFRA 2024'
WHERE NOT EXISTS (SELECT 1 FROM emission_factor WHERE category = 'TRANSPORT' AND sub_category = 'Diesel Truck');
