
# Script for getting Denmark Energinet Network.

import geopandas as gpd

def get_dk_lines_stations(savetofolderpath='', lines_filename='dk_lines.csv', stations_filename='dk_stations.csv'):
    ''''''

    # Set request urls for lines and cables.
    line_url = 'https://agis.energinet.dk/server/rest/services/INSPIRE/XP_el_Inspir/MapServer/0/query?where=OBJECTID+%3E+0&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=OBJECTID%2C+Shape%2C+Byggenavn%2C+Driftssp%C3%A6nding%2C+Shape_Length%2C+DGD_TIMESTAMP&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson'
    cable_url = 'https://agis.energinet.dk/server/rest/services/INSPIRE/XP_el_Inspir/MapServer/1/query?where=OBJECTID+%3E+0&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=OBJECTID%2C+Shape%2C+Byggenavn%2C+Spaending%2C+Shape_Length%2C+DGD_TIMESTAMP&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson'
        
    # Get line data.
    gdf = gpd.read_file(line_url)
    gdf['Type'] = 'line'
    gdf = gdf.rename(columns={'Driftsspænding':'Spaending'})

    # Get cable data.
    gdf2 = gpd.read_file(cable_url)
    gdf2['Type'] = 'cable'

    # Append cabledata to linedate in total gdf.
    lines_gdf = gdf.append(gdf2).reset_index(drop=True)

    # Set request url for stations.
    url = 'https://agis.energinet.dk/server/rest/services/INSPIRE/WMS_WFS_TowerSubstationLine_N/MapServer/1/query?where=OBJECTID+%3E+0&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=OBJECTID%2C+Shape%2C+SubtypeCD%2C+DATECREATED%2C+DATEMODIFIED%2C+NAME%2C+Description%2C++Base_Voltage%2C+DGD_TIMESTAMP&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson'

    # Set type decoder.
    typemap = {
        1 : 'Transformer substations',
        2 : 'Switching substations',
        3 : 'Satellite substations',
        4 : 'AC/DC substations'
    }

    # Get data as GeoDataFrame

    stations_gdf = gpd.read_file(url)

    # Remap the station types.
    for key, val in typemap.items():

        stations_gdf[stations_gdf['SubtypeCD'] == key]['SubtypeCD'] = val

    return lines_gdf, stations_gdf

def main():
    ''''''

    dk_lines, dk_stations = get_dk_network()
    print(dk_lines)

if __name__ == "__main__":
    main()
