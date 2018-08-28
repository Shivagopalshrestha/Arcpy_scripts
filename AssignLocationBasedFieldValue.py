import arcpy

# Set overwrite option
arcpy.env.overwriteOutput = True

# KEEPING ORIGINAL LAYERS (NOT CREATING ADDITIONAL "JOINED" LAYER)
# Create FeatureLayers
arcpy.MakeFeatureLayer_management(<<path to layer to be edited>>, "lyr_24k")
arcpy.MakeFeatureLayer_management(<<path to layer where the edits are coming from>>, "lyr_100k")

# Add field   (remove this if the field already exists...)
arcpy.AddField_management("lyr_24k", "Quad_100k", "TEXT", "", "", "100")

# Create a search cursor for the states
rows = arcpy.SearchCursor("lyr_100k")
for row in rows:
    # Select each 100k quad one at a time, and then select all the 24k quads in that 100k quad and calculate the 'Quad)100k' field
    # NOTE: If you are using not using shapefiles, then you'll have to change the FID in the line below to OBJECTID (or similar)
    arcpy.SelectLayerByAttribute_management("lyr_100k", "NEW_SELECTION", "\"FID\" = " + str(row.getValue("FID")))
    arcpy.SelectLayerByLocation_management("lyr_24k", "HAVE_THEIR_CENTER_IN", "lyr_100k", "", "NEW_SELECTION")
    arcpy.CalculateField_management("lyr_24k", "Quad_100k", "'{0}'".format(str(row.getValue("QUAD_NAME"))), "PYTHON_9.3", "")
    print "Finished processing " + str(row.getValue("QUAD_NAME")) 

