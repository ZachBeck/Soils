
# Function no longer needed since schema won't hold pH values
# from ph_to_mapunit import get_pH

import arcpy

def get_pH(ugrc_soils):

    def return_zero(word):
        if word == None:
            word = 0
        return word

    ssurgo_gdb = r'C:\ZBECK\SGID\Soils\gSSURGO\gSSURGO_UT.gdb'
    mupolygon = ugrc_soils
    print(mupolygon)

    with arcpy.EnvManager(workspace=ssurgo_gdb):
        arcpy.env.overwriteOutput = True

        mapunit_tbl = 'mapunit'
        horizon_tbl = 'chorizon'
        component_tbl = 'component'

        mapunit_to_component = {row[0]:[] for row in arcpy.da.SearchCursor(mupolygon, ['MUKEY'])}
        component_to_mapunit = {}

        with arcpy.da.SearchCursor(component_tbl, ['cokey', 'mukey']) as scursor:
            for row in scursor:
                component_to_mapunit[row[0]] = [row[1]]
    
                if row[1] in mapunit_to_component:
                    mapunit_to_component[row[1]].extend([row[0]])

        cokey_pH = {}
        with arcpy.da.SearchCursor(horizon_tbl, ['cokey', 'hzdept_r', 'ph1to1h2o_r']) as scursor:
            for row in scursor:
                if row[1] == 0:
                    if row[0] not in cokey_pH:
                        cokey_pH[row[0]] = [round(return_zero(row[2]), 1)]
        print(cokey_pH)
        
        mapunit_ph = {}
        for co_key in cokey_pH:
            if co_key in component_to_mapunit:
                if component_to_mapunit[co_key][0] not in mapunit_ph:
                    mapunit_ph[component_to_mapunit[co_key][0]] = cokey_pH[co_key]
                else:
                    mapunit_ph[component_to_mapunit[co_key][0]].extend(cokey_pH[co_key])

        for munit in mapunit_ph:
            if 0 in mapunit_ph[munit]:
                mapunit_ph[munit].remove(0)
            mapunit_ph[munit] = sorted(mapunit_ph[munit])

        print(mapunit_ph)

        return mapunit_ph

