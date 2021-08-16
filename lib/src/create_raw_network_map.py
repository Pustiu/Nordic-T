
# Module for creating maps from


def create_raw_network_map():
    '''Creates folium map of raw network sources'''

    # Importing libraries.
    import folium
    from folium import plugins

    # Creating empty folium map with added basemap tilelayers.
    m = folium.Map(location=[63.5, 17], zoom_start=4, tiles='cartodbpositron', minResolution=0)

    # Add Finland, Fingrid Network to map.
    navici_wms_url = 'https://fingrid.navici.com/wms/3d5805c1f9cda9db42d9d9378952427b'
    fi_fg = folium.FeatureGroup(name='Finland, Fingrid Grid')
    fi_fg.add_to(m)
    folium.WmsTileLayer(url=navici_wms_url, 
                    attr='<a href="https://fingrid.navici.com/">Fingrid Navici</a>',
                    layers=['active_power_lines', 'external_power_lines', 'active_cables', 'external_cables', 'active_stations', 'external_stations'], 
                    transparent=True, fmt='image/gif').add_to(fi_fg)

    # Add Denmark, Energinet Network to map.
    dk_lines_url = 'https://agis.energinet.dk/server/services/INSPIRE/XP_el_Inspir/MapServer/WMSServer'
    dk_stations_url = 'https://agis.energinet.dk/server/services/INSPIRE/WMS_WFS_TowerSubstationLine_N/MapServer/WMSServer'
    dk_fg = folium.FeatureGroup(name='Denmark, Energinet Grid')
    dk_fg.add_to(m)

    folium.WmsTileLayer(url=dk_lines_url, 
                    attr='<a href="https://agis.energinet.dk/server/rest/services/"> Energinet ArcGIS</a>',
                    layers=['0', '1', '2', '3'], 
                    transparent=True, fmt='image/gif').add_to(dk_fg)
    folium.WmsTileLayer(url=dk_stations_url, 
                    #attr='<a href="https://agis.energinet.dk/server/rest/services/"> Energinet ArcGIS</a>',
                    layers=['1'], 
                    transparent=True, fmt='image/gif').add_to(dk_fg)

    # Add Norway, Statnett Network to map.
    no_url = 'https://nve.geodataonline.no/arcgis/services/Nettanlegg2/MapServer/WMSServer'
    no_fg = folium.FeatureGroup(name='Norway, Statnett Grid')
    no_fg.add_to(m)
    folium.WmsTileLayer(url=no_url, 
                    attr='<a href="https://nve.geodataonline.no/arcgis/rest/services/Nettanlegg2/MapServer">Statnett/Nve ArcGIS</a>',
                    layers=['Sjokabler', 'Distribusjonsnett', 'Regionalnett', 'Sentralnett', 'Transformatorstasjoner', 'Master og stolper'], 
                    transparent=True, fmt='image/png', minZoom=0).add_to(no_fg)

    # Add Sweden, SvK Network to map.
    se_fg = folium.FeatureGroup(name='Sweden, Svenska Kraftnät Grid')
    m.add_child(se_fg)
    se_wms_layer = folium.WmsTileLayer(url='https://inspire-skn.metria.se/geoserver/skn/wms', 
                    attr='<a href="https://inspire-skn.metria.se/geoserver/skn/wms?REQUEST=GetCapabilities">Svenska Kraftnät/Läntmäteriet GeoServer</a>',
                    layers=['US.ElectricityNetwork.Lines', 'US.ElectricityNetwork.StationAreas', 'US.ElectricityNetwork.Stations'], 
                    transparent=True, fmt='image/gif')
    se_fg.add_child(se_wms_layer)


    # Add layer control to map.
    folium.LayerControl(collapset=False).add_to(m)
    #plugins.Draw().add_to(m)
    plugins.MeasureControl(position='bottomleft').add_to(m)
    plugins.Fullscreen().add_to(m)

    return m


def main():
    ''''''
    from inspect import getsourcefile
    import os
    import webbrowser

    # Get Map.
    m = create_raw_network_map()

    # Get absolute path to this script, a.
    this_path = os.path.dirname(getsourcefile(lambda:0))

    # Get path to data map
    filepath = os.path.join(this_path, 'raw_network_map.html')
    print(this_path)
    #this_path = os.path.dirname(__file__)

    # Save map to file.
    m.save(filepath)

    webbrowser.open(filepath)

    pass

if __name__ == '__main__':
    main()

