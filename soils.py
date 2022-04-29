import arcpy
import pandas as pd
import os
'''
No longer needed since schema won't hold pH values
from ph_to_mapunit import get_pH
'''

def remove_null(word):
    if word == None:
        word = ''
    return word

ssurgo_db = r'C:\ZBECK\SGID\Soils\gSSURGO\gSSURGO_UT.gdb'
mupoly_fc = os.path.join(ssurgo_db, 'MUPOLYGON')
mapunit_tbl = os.path.join(ssurgo_db, 'mapunit')
muaggatt_tbl = os.path.join(ssurgo_db, 'muaggatt')
coecoclass_tbl = os.path.join(ssurgo_db, 'coecoclass')

ugrc_soils_fc = r'C:\ZBECK\SGID\Soils\Soils.gdb\Soils'
# ugrc_soils_flds = ['mukey', 'areasymbol', 'areaname', 'musymbol', 'muname', 'musurftexgrp', 
#                    'hydgrpdcd', 'engdwbml', 'aws025wta', 'aws050wta', 'aws0100wta',
#                    'aws0150wta', 'hydclprs', 'farmlndcl', 'wtdepannmin', 'wtdepaprjunmin',
#                    'top_ph1to1h2o_r', 'SHAPE@']
ugrc_soils_flds = ['mukey', 'areasymbol', 'areaname', 'musymbol', 'muname', 'musurftexgrp', 
                   'hydgrpdcd', 'engdwbml', 'aws025wta', 'aws050wta', 'aws0100wta',
                   'aws0150wta', 'hydclprs', 'farmlndcl', 'wtdepannmin', 'wtdepaprjunmin',
                   'SHAPE@']
                   
nrcs_query_results = r'C:\ZBECK\SGID\Soils\SoilsQueryResults.csv'
nrcs_query_df = pd.read_csv(nrcs_query_results)
nrcs_query_dict = nrcs_query_df.set_index('mukey').T.to_dict('list')

'''
nrcs dictionary structure
nrcs_query_dict = {mukey: ['areasymbol', 'areaname', 'musym', 'muname', 'mu_dcd_surftexgrp', 'muname',
                           'farmlndcl', 'hydgrpdcd', 'engdwbml', 'aws025wta', 'aws050wta', 'aws0100wta',
                           'aws0150wta', 'hydclprs', 'wtdepannmin', 'wtdepaprjunmin']}
'''

mupoly_flds = ['MUKEY', 'AREASYMBOL', 'MUSYM', 'SHAPE@']
mapunit_flds = ['mukey', 'muname', 'farmlndcl']
muaggatt_flds = ['mukey', 'hydgrpdcd', 'engdwbml', 'aws025wta', 'aws050wta', 'aws0100wta',
                 'aws0150wta', 'hydclprs', 'wtdepannmin', 'wtdepaprjunmin']
coecoclass_tbl = ['ecoclassname']

arcpy.TruncateTable_management(ugrc_soils_fc)
print('truncated ugrc soils features')

with arcpy.da.SearchCursor(mapunit_tbl, mapunit_flds) as scursor:
    for row in scursor:
        if int(row[0]) in nrcs_query_dict:
            nrcs_query_dict[int(row[0])].extend([row[1], row[2]])
            
with arcpy.da.SearchCursor(muaggatt_tbl, muaggatt_flds) as scursor:
    for row in scursor:
        if int(row[0]) in nrcs_query_dict:
            nrcs_query_dict[int(row[0])].extend([row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])


with arcpy.da.SearchCursor(mupoly_fc, mupoly_flds) as scursor, \
    arcpy.da.InsertCursor(ugrc_soils_fc, ugrc_soils_flds) as icursor:

    for row in scursor:
        mukey = row[0]
        areasymbol = row[1]
        musymbol = row[2]
        shp = row[3]
        # icursor.insertRow((mukey, areasymbol, '', musymbol, '', '', '', '', None,
        #                    None, None, None, '', '', None, None, None, shp))
        icursor.insertRow((mukey, areasymbol, '', musymbol, '', '', '', '', None,
                           None, None, None, '', '', None, None, shp))

with arcpy.da.UpdateCursor(ugrc_soils_fc, ugrc_soils_flds) as ucursor:
    for row in ucursor:

        if int(row[0]) in nrcs_query_dict:
            row[2] = remove_null(nrcs_query_dict[int(row[0])][1])
            row[4] = remove_null(nrcs_query_dict[int(row[0])][3])
            row[5] = remove_null(nrcs_query_dict[int(row[0])][4])
            row[6] = remove_null(nrcs_query_dict[int(row[0])][7])
            row[7] = remove_null(nrcs_query_dict[int(row[0])][8])
            row[8] = nrcs_query_dict[int(row[0])][9]
            row[9] = nrcs_query_dict[int(row[0])][10]
            row[10] = nrcs_query_dict[int(row[0])][11]
            row[11] = nrcs_query_dict[int(row[0])][12]
            row[12] = remove_null(nrcs_query_dict[int(row[0])][13])
            row[13] = remove_null(nrcs_query_dict[int(row[0])][6])
            row[14] = nrcs_query_dict[int(row[0])][14]
            row[15] = nrcs_query_dict[int(row[0])][15]

        ucursor.updateRow(row)

'''
No longer needed since schema doesn't hold pH values
mapunit_ph = get_pH(ugrc_soils_fc)
with arcpy.da.UpdateCursor(ugrc_soils_fc, ugrc_soils_flds) as ucursor:
    for row in ucursor:
        if row[0] in mapunit_ph:
            if mapunit_ph[row[0]] == []:
                row[16] = None
            else:
                row[16] = mapunit_ph[row[0]][0]              
        ucursor.updateRow(row)
'''