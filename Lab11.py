import arcpy

# Set geoprocessing environments
arcpy.env.workspace = r"D:\CU\2024spring\4009gis\Lab\11.python\Lab11_project\Lab11data.gdb"
arcpy.env.overwriteOutput = True
# Define road layers and buffer distance
roads_1980 = "roads1980"
roads_2000 = "roads2000"
buffer_distance = "100 meters"
# Buffer and dissolve all overlaps in the buffer areas
arcpy.Buffer_analysis(roads_1980, "roads1980Buffer", buffer_distance, "", "", "ALL")
arcpy.Buffer_analysis(roads_2000, "roads2000Buffer", buffer_distance, "", "", "ALL")
print("Data are stored in D:\\CU\\2024spring\\4009gis\\Lab\\11.python\\Lab11_project\\Lab11data.gdb")
print("This is a list of road data for buffering: roads1980, roads2000")
# Union habitat and buffer data
landcover = "landcover"
union_output_1980 = "union1980"
union_output_2000 = "union2000"
arcpy.Union_analysis(["roads1980Buffer", landcover], union_output_1980)
arcpy.Union_analysis(["roads2000Buffer", landcover], union_output_2000)
print("This is a list of all input data for UNION function: roads1980Buffer, roads2000Buffer, landcover")
# Select forest land type, excluding parts within buffers
forest_query_1980 = "\"Land_Type\" = 'Forest Land' AND \"FID_roads1980Buffer\" = -1"
forest_query_2000 = "\"Land_Type\" = 'Forest Land' AND \"FID_roads2000Buffer\" = -1"
arcpy.MakeFeatureLayer_management(union_output_1980, "forest_layer_1980", forest_query_1980)
arcpy.MakeFeatureLayer_management(union_output_2000, "forest_layer_2000", forest_query_2000)
print("Areas were selected successfully")
# Calculate total area and assess habitat changes
area_field = "Shape_Area"
stats_table_1980 = "ForestStats1980"
stats_table_2000 = "ForestStats2000"
arcpy.Statistics_analysis("forest_layer_1980", stats_table_1980, [[area_field, "SUM"]])
arcpy.Statistics_analysis("forest_layer_2000", stats_table_2000, [[area_field, "SUM"]])
print("Tables with areas statistics were created successfully")
# Output results
print(f"1980 forest land total area calculation completed, details are stored in table: {stats_table_1980}")
print(f"2000 forest land total area calculation completed, details are stored in table: {stats_table_2000}")

# Additional Calculations for units change and two species
# Add new field "Habitat" to store area in hectares
arcpy.AddField_management(stats_table_1980, "Habitat", "DOUBLE")
arcpy.AddField_management(stats_table_2000, "Habitat", "DOUBLE")
print("Habitat fields added to tables successfully.")
# Calculate "Habitat" field value, converting square meters to hectares
arcpy.CalculateField_management(stats_table_1980, "Habitat", "!SUM_Shape_Area! / 10000", "PYTHON3")
arcpy.CalculateField_management(stats_table_2000, "Habitat", "!SUM_Shape_Area! / 10000", "PYTHON3")
print("Area units converted to hectares successfully.")

# Add new fields "Specie1" and "Specie2" to store the count of two species
arcpy.AddField_management(stats_table_1980, "Specie1", "LONG")
arcpy.AddField_management(stats_table_1980, "Specie2", "LONG")
arcpy.AddField_management(stats_table_2000, "Specie1", "LONG")
arcpy.AddField_management(stats_table_2000, "Specie2", "LONG")
print("Species count fields added to tables successfully.")
# Calculate counts for Species1 and Species2
arcpy.CalculateField_management(stats_table_1980, "Specie1", "!Habitat! / 1", "PYTHON3")
arcpy.CalculateField_management(stats_table_1980, "Specie2", "!Habitat! / 5", "PYTHON3")
arcpy.CalculateField_management(stats_table_2000, "Specie1", "!Habitat! / 1", "PYTHON3")
arcpy.CalculateField_management(stats_table_2000, "Specie2", "!Habitat! / 5", "PYTHON3")
print("Species counts calculated successfully.")

# Final output message
print("All processing steps completed successfully!!!!!!!!!")