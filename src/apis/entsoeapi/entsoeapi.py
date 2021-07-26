'''Api-wrapper module for entsoe-e transparency platform.'''

from datetime import datetime, timedelta
import difflib
import requests
import pandas as pd
import bs4
from bs4 import NavigableString
import json
import geopandas as gpd
import pandas as pd
import numpy as np
from ratelimit import limits
import unicodedata
import re



class EntsoeClient():
    '''Client for Entsoe API'''
    
    #####################
    # Init functions
    #####################
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = f'https://transparency.entsoe.eu/api?'

        # Getting API guide requests and parameters from
        # Webscraping html api-guide url.
        self.api_requests, self.api_parameters = self._get_entsoe_api_statics_guide()
        
        # Retrieving entsoeapi areas GeoDataFrame
        self.entsoeapi_areas_gdf = gpd.read_file("https://raw.githubusercontent.com/ocrj/entsoeapi/main/data/areas/areas.geojson")
        
        # Adding representative points to entsoe areas GeoDataFrame
        self.entsoeapi_areas_gdf['coords'] = self.entsoeapi_areas_gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
        self.entsoeapi_areas_gdf['coords'] = [coords[0] for coords in self.entsoeapi_areas_gdf['coords']] 
        
        # Adding area type, either MBA og CA.


        return None
    
    def get_physical_flows(self, from_area, to_area, start, end):
        '''
        Function:
            Requesting physical flows.

        Service name: 
            4.2.15. Physical Flows [12.1.G]
        
        '''

        # Get matched area codes
        from_area_name, from_area_code = self.find_parameters_match(parameter=from_area, parameter_type="Areas")
        to_area_name, to_area_code = self.find_parameters_match(parameter=to_area, parameter_type="Areas")

        # If a area is not matched.
        if from_area_code is None or to_area_code is None:
            
            # Cannot perform request on non existing area, return None
            return None

        # Setting request parameters.
        parameters = {
            'documentType': 'A11', 
            'in_Domain': from_area_code,
            'out_Domain': to_area_code,
            'periodStart': start,
            'periodEnd': end
        }
        
        # Making request
        response = self._call_api(parameters_dict=parameters)

        # If response is not ok.
        if response.ok == False:

            return None

        
         # Parse raw response from xml to DataFrame.
        df = self.parse_entsoe_response_to_df(soup_parent = response)
        
        # Remap response codes to values.
        df = self.remap_df_parameters(df=df, 
        column_type_mapping = {
            'timeseries-in_domain.mrid': 'Areas',
             'timeseries-out_domain.mrid': 'Areas',
        }
        )

        # Create DataSeries of Exchange values.
        #exchanges = df["point-quantity"].astype(int)

        # Create Dataseries of Exchange values timeintervals
        #time_starts = df["timeinterval-start"].astype(datetime) + timedelta(hours=df["point-position"].astype(int))
        #print
        #time_ends = df["timeinterval-start"].astype(datetime) + 
        #timeintervals = pd.Interval(
        #    df["timeinterval-start"].astype(datetime),

        #)

        # Create list of timeinterval_starts
        # Merging datapoints in DataFrame into one row DataSeries.
        #timeinterval_starts = df["timeinterval-start"]
        #timeinterval_ends =  
        



        return df

            
    def get_generations(self, in_area, start, end):
        '''
        Getting Production 
        '''

        pass


    def request_actual_total_load(self, OutBiddingZone_Domain, PeriodStart=None, PeriodEnd=None):
        '''
        Function for requesting 4.1.1. Actual Total Load [6.1.A]
        '''

        mandatory_parameters = {
            'DocumentType': 'A65',
            'ProcessType': 'A16',
        }


    def get_loads(self, in_areas, start_time=None, end_time=None):
        '''
        Function for getting loaddata for a area.
        '''
        pass


    def _get_entsoe_guide_raw_content(self, url="https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html"):
        '''Gets raw html content in Entsoe Statics Guide Web Page.'''
        
        # Get html content from on entsoe transparency guide web page.
        r = requests.get(url)

        # Try to extract static-content on page.
        try:
            guide_soup = bs4.BeautifulSoup(r.text, "lxml").find('div', {'id': 'static-content'})
        
        # Except not found in content.
        except(AttributeError, TypeError):
            # Print errormessage and return None.
            print(f"ERROR: No guide content found on guide web page, page may be down at \nurl: {url}")
            return None
        


          

    def get_entsoe_statics_guide(self, url="https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html"):
        '''
        Gets updated api statics from statics guide web page, ensuring allways correct and updated use of service.
        '''
        
        
        r = requests.get(url)
        

        # Try to find content and chapter tags in html content soup.
        try:
            # Navigate to page content tag.
            content = bs4.BeautifulSoup(r.text, "lxml").find('div', {'id': 'content'})
            
            # Make list of all guide sections tags.
            hs = content.find_all(lambda x: 'h' in x.name and x.string is not None and len(x.string) > 2)

            # Make list of all header tags used in html content.
            hs_names = list(dict.fromkeys([x.name for x in content.find_all(lambda x: 'h' in x.name)]))
        
        # Except not found in content.
        except(AttributeError, TypeError):

            # Print errormessage and return None.
            print(f"ERROR: No guide content found on guide web page, page may be down at \nurl: {url}")
            return None


        def print_dict(d, istr=''):
            '''Print nested dictionaries.'''
            # Loop on ey, value in dict.
            for key, value in d.items():

                # If value is dict.
                if isinstance(value, dict):

                    # Print layerstring and key.
                    print(f'{istr}{key}')
                    
                    # Print nested dict.
                    print_dict(value, '-'+istr)

                # Else value not dict.
                else:

                    # Print layerstring, key and value.
                    print(f'{istr}{key} = {value}')
                    

        # Make dict for storing statics guide content.
        guide_dict = {}
        
        # Loop on all chapter tags.
        for c in range(len(hs)):
            
            # Store reference to guide_dict.
            nest_dict = guide_dict
                
            # Loop on possible layer tag.names in content.
            for c2 in range(len(hs_names)):

                # If tag.name is not this layer name.
                if str(hs[c].name) != hs_names[c2]:
                    
                    # Walk down to next layer at key in dict.
                    nest_dict = nest_dict[list(nest_dict.keys())[-1]]

                # Else, tag.name is this layer name.
                else:

                    # Add tag.name as this dict layer keys.
                    nest_dict[hs[c].string] = {}
                    
                    
                    print(len(hs[c].find_next_siblings('div')))
                    

                    # Break loop.
                    break


        # Print dict
        print_dict(guide_dict)
        

    def get_entsoe_services(self, url="https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html"):
        pass









        


    
    def parse_entsoe_response_to_df(self, soup_parent, start_tag="", df=pd.DataFrame([]), c_layer=0, layer_children=None):
        '''Helperfunction, recursively parse entso-e api response to pd.DataFrame.'''

        # If input is not soup, make soup.
        if isinstance(soup_parent, str):
            soup_parent = bs4.BeautifulSoup(soup_parent, features="lxml")
        elif isinstance(soup_parent, requests.Response):
            soup_parent = bs4.BeautifulSoup(soup_parent.text, features="lxml")
    
        # If start_tag is not None, this is first run.
        if start_tag is not None:

            

            # If spesified start_tag is not empty string
            if len(start_tag) > 0:

                # Ensure starttag is lowered as response tags are all lowered.
                start_tag = start_tag.lower()

                # Set spesified start_tag as soup_parent
                soup_parent = soup_parent.find(start_tag)
            
            # If spesified start_tag is empty string.
            else:

                # Find response body.
                body = soup_parent.find("body")

                # Set first tag after body, the response document type, as default parsing start parent.
                for child in body.children:
                    soup_parent = child
                    break
            
        
            # Initiate counter to keep track on present recursive layer through parsing.
            c_layer = 0
       


        # Increment layer counter and start search in soup_parent's children.
        c_layer += 1
        for child in soup_parent.children:
            #print(child.name)
            # Skipping bastard children.
            if child.name == None or child.name == '\n':
                continue
        
            # If: this child has multiple descendants, recursively walk down to childs childs childrens layer.
            if len(list(child.descendants)) > 1:

                # Include df in walk down and return from layer.
                df  = self.parse_entsoe_response_to_df(soup_parent=child, df=df, start_tag=None)
            
                # Returned from level, decrement level counter
                c_layer -= 1
        
            # Else: no descendants, add childs content to df. and new child name, add to df.columns as combo of parent and childs name.
            else:
            
                # Content name is combo of parent and childs name.
                column = str(soup_parent.name) + "-" + str(child.name)
            
                # Content value is childs content.
                value = str(child.string)
            
                # If: column not in df.columns, add as new column.
                if column not in df.columns:
                    df[column] = ""
                
                    # If: first input, df has no index, add value directly.
                    if len(df.index.values.tolist()) < 1:
                        df[column] = [value]
                
                    # Else: find index of last row, add value to column cell at last row.
                    else:
                        rowidx = df.index.tolist()[-1]
                        df.at[rowidx, column] = value
            
                # Elif: column is in df.columns but column cell at last row already has content.
                elif pd.isnull(df.iloc[-1:][column].values.tolist()[0]) == False:
                
                    # Append new empty row at end of df for storing new row of data.
                    df = df.append(pd.Series(dtype = 'object'), ignore_index=True)
                
                    # Copy data from upstream level columns to upstream cells in the new empty row in loop.
                    rowidx = df.index.tolist()[-1]
                    cols_list = df.columns.values.tolist()
                    for col_c in range(len(cols_list)):
                        df.at[rowidx, cols_list[col_c]] = df.at[rowidx-1, cols_list[col_c]]
                    
                        # If: loop reached the column of new data content, add the new data in cell, break out of loop and stop copying.
                        if column == cols_list[col_c]:
                            df.at[rowidx, cols_list[col_c]] = value
                            break
            
                # Else: column is in df.columns, and is without content. 
                else:
                
                    # Add content to cell
                    rowidx = df.index.tolist()[-1]
                    df.at[rowidx, column] = value
                    
            
            
        # If returning from top layer, fix finished df before returning.
        if c_layer == 0:
            #df.drop(columns="mrid", axis=0, inplace=True)
            df.replace("", np.nan, inplace=True)
            df.drop_duplicates(inplace=True)

            # Loop on df columns.
            for column in df.columns:

                # Try if column string is valid float, then set as float.
                try:
                    float(df.at[0, column])
                    df[column] = df[column].astype(float)
                
                # If not, do nothing
                except ValueError:
                    None
                
                # Try if column string is valid integer, then set as integer.
                try:
                    int(df.at[0, column])
                    df[column] = df[column].astype(int)
                
                # If not, do nothing
                except ValueError:
                    None
                
                

                    
    
        # Return one layer up.
        return df
    
    def remap_df_parameters(self, df, column_type_mapping = {}):
        '''Helperfunction for remapping response codes to meaning'''
    
        # Storing list of existing columns_names and api parameter_types.
        df_cols_list = df.columns.values.tolist()
        api_para_list = list(self.api_parameters.keys())
    
        # Loop on df rows by index.
        for idx in df.index:
        
            # Loop on spesified columns to type mappings.
            for column, paramtype in column_type_mapping.items():

                # If spesified column exist in df and spesified type exist in available parameter types.
                if column in df_cols_list and paramtype in api_para_list:
            
                # Make sure cell to remap has content, is not already remapped and not empty string.
                    if pd.isnull(df.at[idx, column]) == False and len(df.at[idx, column]) > 0:
                
                        # Make sure cell value is not already mapped:
                        if df.at[idx, column] not in list(self.api_parameters[paramtype].values()):
                    
                            # Remap cell value.
                            df.at[idx, column] = self.api_parameters[paramtype][df.at[idx, column]]
    
        # Return remapped df.
        return df

    #####################
    # Shower functions
    #####################
    def show_parameters(self):
        '''Prittyprints available API parameters'''

        print("-Available API Parameters-")
        for _type, _param in self.api_parameters.items():
            print(f"\n{_type}")
            print(json.dumps(_param, indent=2, default=str))
        return None

    #####################
    # Setter functions
    #####################
    def set_api_key(self, api_key):
        '''Sett api_key'''
        self.api_key = api_key

    #####################
    # Getter functions
    #####################
    def get_from_raw_input(self, url = None, parameters_dict=None, remap=False):
        '''Makes get request from raw inputs, either from constructed url or parameters_dict.
        Input: url or parameters_dict.
        Output: df (None if missing input.)
        '''
        # Making call to api from raw inputs.
        
        response = self._call_api(url=url, parameters_dict=parameters_dict)
        
        # Parsing response xml_html to dict.

        response_dict = self._parse_xml_html_to_dict(response_xml_html=response)
        
        # Remaps response codes to their mapped meanings.

        if remap:
            response_dict = self._remap_response_dict(response_dict)
        
        # Return response dict.

        return response_dict
    
    def get(self, request, from_area, from_time=None, to_area=None, to_time=None, input_parameters_dict=None, raise_exceptions=False, *args, **kwargs):
        '''Function for getting data from entsoe-api, returnes df.
        '''
        # if not spesified from_time, set time to yesterday.
        if from_time is None:
            from_time = datetime.now() - timedelta(1)
        

        # create list for storing: areas, datetimes.
        request_areas = []
        request_datetimes = []


        # search for request match in available request methods.
        request_match = self.find_request_match(request=request)
        

        # search for area match in available parameter areas.
        from_area_match, parameter_type_match = self.find_parameters_match(parameter=from_area, parameter_type='area', return_key1_or_value0=True)
        request_areas.append(from_area_match)
        if to_area is not None:
            to_area_match, to_area_type = self.find_parameters_match(parameter=from_area, parameter_type='area', return_key1_or_value0=True)
            request_areas.append(to_area_match)
        

        # search for request parameters mandatory, optional, structure parameters and fill in parameters_dict
        request_parameters_dict = self._fill_request_parameters(request_match=request_match, input_parameters_dict=input_parameters_dict)


        # ensure correct

        
        # if no match: raise exception errormessage or return None
        if request_match is None:
            if raise_exceptions:
                raise Exception(f'\nERROR: Found no match for your request "{request}".\n Request must resemble one in available api_requests:\n {self.return_show_available_requests(show_df=True, return_df=False)}')
            return None
        elif from_area_match == 'bad_parameter_type':
            if raise_exceptions:
                raise Exception(f'\nERROR: Found no match for your parameter-type "{0}".\n Request must resemble one in available api_requests:\n {self.return_show_available_parameter_types(show_df=True, return_df=False)}')
            return None
        elif from_area_match == 'bad_parameter':
            if raise_exceptions:
                raise Exception(f'\nERROR: Found no match for your parameter "{request}".\n Request must resemble one in available api_requests:\n {self.return_show_available_parameter(parameter_type=parameter_type_match, show_df=True, return_df=False)}')
            return None
        
        # if match found, get api_request info, mandatory and available parameters


        ######################
        ######################

    def create_recursive_family_tag_to_family_tree_dict(self, family_tag, family_name=None, family_tree_dict = {}):
        '''
        Recursive function for creating a dictionary family tree from a BeautifullSoup tag with multiple descendants.
        '''

        layer_family_names = []
        # Loop on family_tag children.
        for child in family_tag.children:

            # Find this layer family names.


            # If child has only one descendant, add child string to family_tree
            if len(list(child.descendants)) == 1:
                layer_family_names.append(child.string)

            
        # Make new loop on family_tag children.
        for child in family_tag.children:

            
            # If child har multiple descendant, add family subtree to the child name in the family_tree_dict.
            if len(list(child.descendants)) > 1:
                #print(f"DESCENDANTS: {child.string}")
                
                family_tree_dict[family_name] = self.create_recursive_family_tag_to_family_tree_dict(family_tag=child, family_name=family_name)

        # Create dict 

            #else:
                #family = 
        
        # Return family_tree_dict upstream the family_tree.
        return family_tree_dict


    
    
    #####################
    # Inner functions
    #####################

    def _insert_value_in_nested_dict(self, original_dict, keys_path_list, value, first=False):
        '''
        Insert value in nested dictionary at end of list with path of keys to follow.
        '''
    
        if first:
            original_dict_ref = original_dict


        
        # Ensure as list.
        if isinstance(keys_path_list, list) == False:
            keys_path_list = [keys_path_list]

        # If inputlist is empty.
        if len(keys_path_list) < 1:
            
            # Return original dict.
            return original_dict
        
        # Store first key in the keys_path_list as this layers key.
        key = keys_path_list[0]
    
        # Remove key from rest of the keys_path_list
        keys_path_list.pop(0)

        # Ensure as list.
        if isinstance(keys_path_list, list) == False:
            keys_path_list = [keys_path_list]
    
        # If key is not in list of this nested keys.
        if key not in list(original_dict.keys()):
        
            # Add key and empty dict value to the nested_dict.
            original_dict[key] = {}
        
        # If there is more keys in keys_path_list.
        if len(keys_path_list) > 0:

            # If this nested dict key value is not dict.
            if isinstance(original_dict[key], dict) == False:

                # Wrap value as dict.
                original_dict[key] = {str(original_dict[key]): {}}

            # Walk down layer
            original_dict = self._insert_value_in_nested_dict(original_dict[key], keys_path_list, value)
            
        # If there is no more keys in keys path list.
        else:

            # Insert key and value to the nested dict.
            original_dict[key] = value

        if first:
            return original_dict_ref
        else:
            # Return edited original dict.
            return original_dict
            
                
        
            
        
        # Return copy of the edited original dict.
        return original_dict.copy()



    def _parse_entsoe_guide_content_to_dict(self, soup_parent, soup_dict={}, layer_value=None, layer_counter=-1, name_class_string_lists_to_keys_dict = {'name': ['h2', 'h3', 'h4'], 'class': [], 'string': []}, name_class_string_lists_to_values_dict = {'name': ['table', 'code'], 'class': [], 'string': []}):
            '''
            Recursive function for parsing Entso-E Static API Guide html content into a dictionary.

            - Each guide headers area added as dict keys.
            - Content within each header is added as nested dict to header key.
            '''
            # Helper functions.
            def _get_dict_path2value_list(_dict, value):
                '''Return list of values until found match'''
                
                # Finding list depth
                value_depth = list(_dict.value()).index(value)

                # Appending values until depth is reached to list.
                path2value_list = []
                c=0
                for key, item in _dict.items():
                    if c <= value_depth:
                        path2value_list.append(item)
                        c+=1
                
                # Returning list of path to value in dict.
                return path2value_list
            

                
            
            # Increment layer_counter
            layer_counter += 1
            #print(layer_counter)

            # Loop on parents children.
            for child in soup_parent.children:

                

                #################################################
                ## Add layer to dict when new layer is reached ##
                #################################################

                # Manuel fix for 1.4. Parameters
                if "1.4. Parameters" in str(child.string) and "1.4. Parameters" not in list(soup_dict.keys()):

                    #print(child.string)

                    if layer_value is None: 

                        # Set this layer as first layer.
                        layer_key = "h3"
                        layer_value = str(child.string)
                        soup_dict[layer_value] = {}
                        #soup_dict[layer_value] = content_dict.copy()
                        #content_dict.from_keys(content_dict, [])

                    else:
                    
                        # Add stored content, set new layer_value. and stored content to dict.
                        #soup_dict[layer_value] = {}
                        print("BLUE")
                        #soup_dict[layer_value] = {}
                        soup_dict[layer_value] = content_dict.copy()
                        content_dict = {key: list() for key in content_dict}
                        #content_dict = content_dict.from_keys(list(content_dict.keys()), [])
                        #content_dict = {}
                        
                        layer_key = "h3"
                        layer_value = str(child.string)
                
                # if child.name in spesified layer_dict,
                elif str(child.name) in name_class_string_lists_to_keys_dict['name']:

                    #print(child.string)
                    

                    # If child.string is not empty and not None.
                    if len(child.string) > 2:
                        
                        if layer_value is None: 

                            # Set this layer as first layer.
                            layer_key = str(child.name)
                            layer_value = str(child.string)
                            #soup_dict[layer_value] = {}
                            soup_dict[layer_value] = content_dict.copy()
                            content_dict = {key: list() for key in content_dict}
                            #content_dict.from_keys(content_dict, [])

                        else:
                    
                            # Add stored content, set new layer_value. and stored content to dict.
                            #soup_dict[layer_value] = {}
                            
                            # Add stored content to this layer.
                            soup_dict[layer_value] = content_dict.copy()
                            content_dict = {key: list() for key in content_dict}
                            
                            # Reset content_dict before storing new layer.
                            #content_dict.from_keys(content_dict, [])
                            
                            # Set new layer key, value
                            layer_key = str(child.name)
                            layer_value = str(child.string)


                
                ###########################################
                ## Parse guide content as dict contents. ##
                ###########################################

                # If current child.name is list of spesified keys to be included in layer content.
                if str(child.name) in list(content_dict.keys()):
                
                    #############
                    ## Tables. ##
                    #############
                    
                    # If child.name is table.
                    if str(child.name) == "table":

                        # If table columns is larger than minimum 1 for table columns. (skip bastard small html infotables.)
                        if len(child.find_all('tr')) > 1:

                            # Create list for storing rows.
                            row_list = []

                            # Find all rows.
                            for row in child.find_all('tr'): 

                                # Create list for storing rows column values.
                                row_col_list = []

                                for row_col_value in row.find_all('td'):
                                    row_col_list.append(row_col_value.text)

                                row_list.append(row_col_list)
                            
                            df = pd.DataFrame(row_list[1:], columns=row_list[0])
                            
                            # Append df to content_dict tables list
                            content_dict["table"].append(df)

                    # If child.name is code table.    
                    elif str(child.name) == "code":
                        
                        content_dict["code"].append(child.text)

                        #print(content_dict["code"])



                    else:
                        pass


                        # Append text content to list of codetags.


                        

                        
                    # If child classes match spesified list of content classes.
                    #if str(child.name) in list(content_dict.keys()):
                        #pass
                    
                
                #####################################################
                ## If child has descendands, call recurse function ##
                #####################################################

                # Try.
                try:
                    # Get child descendants.
                    descendants = child.descendants
                    
                    # Put child as parent and recursively walk down tree.
                    soup_dict, layer_value, layer_counter, layer_dict, content_dict =  self._parse_entsoe_guide_content_to_dict(soup_parent=child, soup_dict = soup_dict, layer_value = layer_value, layer_counter=layer_counter, layer_dict = layer_dict , content_dict = content_dict.copy() )

                    
                    
                # Except.
                except (RuntimeError, TypeError, NameError, AttributeError):
                        
                    # AttributeError: no descendants, do nothing.
                    None
            

            # If last child and top layer.
            #print(layer_counter)
            if child is list(soup_parent.children)[-1] and layer_counter <= 0:

                print("FINISHED")

                # Store last content on present layer.
                soup_dict[layer_value] = content_dict.copy()

                # Return only soup_dict
                return soup_dict
            
            else:
                # If not last child and returning from top layer

                # Return both soup_dict and dict_key
                layer_counter -= 1
                return soup_dict, layer_value, layer_counter, layer_dict, content_dict
           

    def _parse_entsoe_guide_toc_to_df(self, entsoe_guide_soup):
        '''
        
        '''

        ######################################
        ##  Add TOC to statics_guide_dict.  ##
        ######################################

        # Extract toc and toc title.
        toc = entsoe_guide_soup.find(id="toc")
        toc_title = toc.find(id="toctitle").string
        
        # Create DataFrame for storing toc.
        df = pd.DataFrame([], columns=["sectlevel1", "sectlevel2"])
        
        # Get sectlevel1 elements.
        sectlevel1 = toc.find(class_="sectlevel1")
        
        # Loop on the elements.
        for sectlevel1 in sectlevel1.children:

            # Store level name string.
            sectlevel1_name = str(sectlevel1.find("a").string)
            
            # Find sectlevel2 in this sectlevel1.
            sectlevel2 = sectlevel1.find(class_="sectlevel2")

            # If sectlevel2 is not empty.
            if sectlevel2 is not None:

                # Loop on sectlevel2 elements.
                for sectlevel2_name in sectlevel2.find_all("a"):

                    # Append combination of sectlevel1 and sectlevel2 to DataFrame.
                    df = df.append({'sectlevel1': str(sectlevel1_name), 'sectlevel2': str(sectlevel2_name.string)}, ignore_index=True)

            # If sectlevel2 is empty.
            else:
                
                # Append combination of sectlevel1 for both locations levelcolumns in DataFrame.
                df = df.append({'sectlevel1': str(sectlevel1_name), 'sectlevel2': str(sectlevel1_name)}, ignore_index=True)

        # Add toc DataFrame to statics_guide_dict.
        #self.statics_guide_dict[toc_title] = df

        return df

    
    def _get_entsoe_api_statics_guide(self):
        '''
        Getting entsoe api service statics from the api guide webpage using webscraping.
        API guide url: https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html
        '''

        # Create dict for storing Entsoe Transparency Statics Guide Web Page content.
        guide_dict = {}

        # Set url for Entsoe Transparency Statics Guide Web Page.
        url = 'https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html'
        
        # Get html content of Entsoe Transparency API guide web page.
        r = requests.get(url)
        
        # If response is bad, return error_message dict and False flag.
        if r.ok == False:
            return {'error_message': 'bad request response.'}, False

        # Parse html content to bs4.BeatutifulSoup object.
        soup = bs4.BeautifulSoup(r.text, "lxml")

        # Extract part of html content containing the static content.
        static_content = soup.find(id="static-content")

        # If static content is not found in guide html content (api service may be down for maintenance).
        if static_content is None:

            # Return errormessage and False flag.
            return {'error_message': f'static content not found on entsoe statics guide webpage, may be down for maintenance, check source url: {url}.'}, False

        # Get Entsoe Statics Guide TOC as DataFrame 
        
        toc_df = self._parse_entsoe_guide_toc_to_df(entsoe_guide_soup = static_content.find(id="header"))
        
        
        #######################################################################################
        ##  Add static guide content to the statics_guide_dict.  ##
        ######################################################################################

        #print(toc_df)

        static_content_content = static_content.find(id="content")

        # Finding all headers. TODO: missing 1.4. Parameters due du it being nested in ulist. Content included in 1.3.
        headers = static_content_content.find_all(lambda x: x.name in ['h2', 'h3', 'h4'] and len(x.string) > 2)

        for header in headers:
            pass



        # Get list of headers parents.
        header_parents = []
        for header in headers:
            header_parents.append(header.find_parent('div'))

        # Add parents content to the header in dict
        c=0
        for idx in range(len(headers)):
            try:
                guide_dict[headers[idx]] = pd.read_html(header_parents[idx].text)
            except(ValueError): 
                None

        print(guide_dict)
        
        #guide_dict = self._parse_entsoe_guide_content_to_dict(soup_parent = static_content.find(id="content"), )
        
        
        #print("RETURNED DATA")
        #for key, value in statics_guide_dict.items():
            #value_table = value["table"]
            #value_code = value["code"]
            #keys = 
            #print(f"{key} --> {len(value_code)}")
            #print(value)
    
        return None, None


        #print(static_content_content.prettify())

        # Looping on the guide toc.
        for sectlevel2 in df["sectlevel2"]:
            pass

            

        static_content_sections_list = ['sect1', 'sect2', 'sect3', 'paragraph', 'ulist']
        sections_content_list = ['paragraph', 'ulist']

        
        
        
        soup_content_content = static_content.find(id="content")

        
        soup_content = soup.find(id="content")
        
      


        #static_content_content = static_content.find(id="content")
        
        # Extract content in guide chapters and appendix.
        soup_chapters = soup_content.find_all(class_="sect1")
        soup_ch1_ch2 = soup_chapters[:1] #incl: api_url, 
        soup_ch3 = soup_chapters[2]
        soup_ch4 = soup_chapters[3] #incl: possible requests with parameterspesifications and request structure examples.
        soup_apndxA = soup_chapters[4] #incl: parameterslists,
        soup_apndxB = soup_chapters[5]

        # Create dict for storing API guide.
        static_guide = {}

        # Extracting guide TOC.
        #toc = soup.find(id="toc")

        #print(toc.prettify())
        
        #toc_dict = self.create_recursive_family_tag_to_family_tree_dict(toc)

        
        #for key, value in toc_dict.items():
            #print(key)
        
        #for child in toc.children:
        #    print(len(list(child.descendants)))
            #if  < 1:
            #    print(child.text)

        #print(toc[2].name)

        # Extracting guide toc title
        #toctitle_str = soup.find(id="toctitle").text

        # Get TOC table level 1.

        
        #print(toctitle_str)
        
        #for a in toc_soup:
            #print(a)
    
        # Store request endpoint url.
        #endpoints_soup = soup.find(lambda tag: tag.name == "h2" and "1.3. Request endpoints" in tag.text)
        #endpoints_soup = endpoints_soup.find(lambda tag: "Production" in tag.text)
        #for a in endpoints_soup:
        #    print(a.text)
        
        ##############################################################
        #ch4: extract possible requests, parameters and code examples#
        ##############################################################

        services_dict = {}
        # Find all tags for service domains.
        service_domains_soup = soup_ch4.find_all(lambda tag: tag.name == "h3" and "4." in tag.text and "Detailed guidelines and examples" not in tag.text and "A." not in tag.text)
        
        # Add the Service domains as keys in the services_dict.
        for domain in service_domains_soup:
            services_dict[domain.text] = ''

        # Find the service domains subservices.

        
        for key, value in services_dict.items():
            #print(key)
            pass


        #extract part with api_requests info
        requests_data = soup_ch4.find_all(class_="sect2")
        requests_data = requests_data[:8]

        #TODO: add request example structures
        #get list of requests_code_examples from POST examples, dont use GET examples as they vary in html-stylings......
        requests_structure = soup_ch4.find_all(lambda tag: tag.name=="code" and "POST" in tag.text and "java" not in tag.text)
        #print(requests_structure.contents)
        
        #filters and fixes request structure examples. this is based on GET...
        structure_list = []
        for structure in requests_structure:
            #if no multiple descendants: adds to list
            if len(list(structure.descendants)) == 1:
                if structure.contents[0] not in structure_list and len(structure.contents[0]) > 10: #fix: removes empty GET d.t. html-font block..
                    structure_list.append(structure.contents[0])
            
            #else: walk down tree and add descendant due to html-font block..
            else:
                for structure1 in structure:
                    if len(list(structure1.descendants)) == 1:
                        structure_list.append(structure1.contents[0])
            


                    
                    #print(structure.contents[0])
        #print(len(structure_list))
            #print(dir(structure))
            #break
            #dd+=1
        #make list of available request headers, fix text
        requests_headers = []
        for a in requests_data:
            a_headers = a.find_all(lambda tag:tag.name=="h4" and "A." not in tag.text and "B." not in tag.text)
            requests_headers.extend(a_headers)
    
        #fix text, store headers in (for now) empty dict
        api_requests = {}
        for c in range(len(requests_headers)):
            header_text = requests_headers[c].text
            header_text = header_text.replace('\u2009','')
            header_text = header_text.replace('\xa0','')
            header_text = header_text.replace('.','_')
            header_text = header_text.replace('&','_')
            header_text = header_text.replace(' ','_')
            header_text = header_text.replace('__','_')
            header_text = header_text #do not lower, lower only on search.
            requests_headers[c] = header_text
            api_requests[header_text] = None

        #getting requests parameters info, mandatory, optional
        api_requests_keys = list(api_requests.keys())
        count=0
        for a in range(len(requests_data)):
            requests_info = []
            requests_mandatory = []
            requests_optional = []
    
            #extract list of data on info, mandatory, optional
            requests_info_mandatory_optional_data = requests_data[a].find_all(class_="ulist")
    
            #make dict for storing parameters
            param = {} 
    
            #loop lists of data on info, mandatory, optional
            for b in range(len(requests_info_mandatory_optional_data)):
                requests_info = []
                requests_mandatory = []
                requests_optional = []
        
                #extract each textline on info, mandatory, optional
                requests_info_mandatory_optional = requests_info_mandatory_optional_data[b].find_all('p')
                
                #fix: if not key='Mandatory parameters' in list, skip this duplicate nested class_="ulist" 
                storedata=False
                for c in range(len(requests_info_mandatory_optional)):
                    if 'mandatory parameters' in requests_info_mandatory_optional[c].text.lower(): #skips each table in main table
                        storedata=True
                        
                # if not skipped, store info, mandatory, optional data
                if storedata and count <= (len(api_requests_keys)-1):
                    
                    #using flags to seperate data in different textstrings
                    infoflag=True
                    mandatoryflag=False

                    #loop on textstrings
                    for c in range(len(requests_info_mandatory_optional)):
                
                        #cleanup textstring
                        text_string = requests_info_mandatory_optional[c].text
                        text_string = text_string.replace('\xa0','')
                        text_string = text_string #this is parameters, do not lower, never alter parameters.
                
                        # if key='Mandatory' in textstring, set mandatoryflag and continue to next iter
                        if 'Mandatory' in text_string:
                            infoflag=False
                            mandatoryflag=True
                            continue
                
                        # if key='Optional' in textline, reset mandatoryflag and continue to next iter
                        elif 'Optional' in text_string:
                            mandatoryflag=False
                            continue
                
                        #store textlines based on key flags.
                        if infoflag:
                            requests_info.append(text_string)
                        elif mandatoryflag:
                            requests_mandatory.append(text_string)
                        else:
                            requests_optional.append(text_string)
                    
                    #store in parameter dict
                    param['info'] = requests_info
                    param['mandatory'] = requests_mandatory
                    param['optional'] = requests_optional
                    #param['structure'] = requests_structure[count] TODO: add when sorted above.
                    
                    #add to main dict
                    api_requests[api_requests_keys[count]] = param
                    count+=1
        
        #add main dict as attribute
        setattr(self, 'api_requests', api_requests)

        ################################################################
        ################################################################

        ##################################################
        #apndxA: extract api parameters headers and tables#
        ##################################################
        param_headers = soup_apndxA.find_all(lambda tag:tag.name=="h3" and "A." in tag.text)
        param_tables = soup_apndxA.find_all("table")
        param_dflist = pd.read_html(str(param_tables))

        #remove small info tables and sort:
        templist = []
        a = 0
        for c in range(len(param_dflist)):
            if len(param_dflist[c]) > 2: #removes small unwanted texttables.
                param_dflist[c].columns = param_dflist[c].iloc[0] #add first row as columns
                param_dflist[c] = param_dflist[c].drop(0) #drop old first row
                #param_dflist[c] = param_dflist[c].applymap(str.lower) #ensure all strings lower
                param_dflist[c].name = param_headers[a].text #add list name as df.name
                a=a+1 #header counter
                templist.append(param_dflist[c])
        param_dflist = templist
        del templist

        #store in api_variables as nested dict.
        api_parameters = {}
        for df in param_dflist:
            df_name = df.name
            df_name = df_name.split(' ', 1)[1] #remove table number A.1, A.2 etc.
            df_name = df_name.split(', ', 1) #if multiple api arguments is same list of parameters, split and create one for each.
            df_dict = dict(zip(df.iloc[:,0],df.iloc[:,1]))
            for name in df_name:
                for keys, values in df_dict.items(): #cleanup unicode
                    keys = keys.replace('\xa0',' ')
                    values = values.replace('\xa0',' ')
                    df_dict[keys] = values
                api_parameters[name] = df_dict
                
        setattr(self, 'api_parameters', api_parameters)

        return api_requests, api_parameters

        ######################################
        ######################################
                
    def _scrape_parameters_lists(self):
        '''Scrape parameters lists
        '''
        pass
            
    def _find_request_parameters(self, request_match, input_parameters_dict):
        '''Finds and returns filtered mandatory and optional parameters for request call
        '''
        #finds requests mandatory, optional and structure
        mandatory_parameters = self.api_request[request_match]['mandatory']
        optional_parameters = self.api_request[request_match]['optional']
        request_structure = self.api_request[request_match]['structure']

        #loop filter mandatory parameters
        mandatory_list = []
        for c in range(len(mandatory_parameters)):

            #in case of string, split into list of words and extract on keywords.
            words = c.split(' ')
            if len(words) > 1:
                    
                #if: check for Period (PeriodStart and/or PeriodEnd)
                word_match = difflib.get_close_matches('Period', words, n=2, cutoff=0.6) #extract if PeriodStart and PeriodEnd
                if len(word_match) > 0:
                    for match in word_match:
                        mandatory_list.append(match)
                    
                #else: check for Time (TimeInterval)
                else:
                    word_match = difflib.get_close_matches('Time', words, n=2, cutoff=0.6) #extract if PeriodStart and PeriodEnd
                    if len(word_match) > 0:
                        for match in word_match:
                            mandatory_list.append(match)

            #else not string: add mandatory to mandatory_list
            else:
                mandatory_list.append(mandatory_parameters[c])

        #loop filter optional parameters
        optional_list = []
        for c in range(len(optional_parameters)):

            #in case of string, split into list of words and extract on keywords.
            words = c.split(' ')
            if len(words) > 1:
                    
                #if: check for Period (PeriodStart and/or PeriodEnd)
                word_match = difflib.get_close_matches('Period', words, n=2, cutoff=0.6) #extract if PeriodStart and PeriodEnd
                if len(word_match) > 0:
                    for match in word_match:
                        optional_list.append(match)
                    
                #else: check for Time (TimeInterval)
                else:
                    word_match = difflib.get_close_matches('Time', words, n=2, cutoff=0.6) #extract if PeriodStart and PeriodEnd
                    if len(word_match) > 0:
                        for match in word_match:
                            optional_list.append(match)

            #else not string: add optional to optional_list
            else:
                optional_list.append(optional_parameters[c])

        structure_dict = {}
        #loop filter structure dict
        a = request_structure.split("?") #get parameters part after "?"
        a = a.split(";&amp") #get each "param=value"
        
        #loop to split {'param': 'value'}, store in in structure_dict
        for b in a:
            b = b.split("=")
            structure_dict[b[0]] = b[1]

        #return lists
        return mandatory_list, optional_list, structure_dict
        ######################################

    def _fill_request_parameters(self, request_match,  input_parameters_dict): #TODO
        '''Finds, fills and returns mandatory and optional parameters for requested call.
        '''
        #finds filtered mandatory and optional parameters lists
        mandatory_list, optional_list, request_structure = self._find_request_parameters(request_match=request_match)

        #fills in request_parameters_dict TODO
        request_parameters_dict = {}

        return request_parameters_dict

    def find_request_match(self, request, n_matches=1, accuray_matches=0.4):
        ''' Finds closest match in avaialable api_requests, returns match.
        If no match, raise display of available api_requests.
        '''
        #fix remove spaces and set all capital letters to lower
        request_lower = request.replace(' ','_')
        request_lower = request.lower()
        requests_list = list(self.api_requests.keys())
        requests_list_lower = [each_string.lower() for each_string in requests_list]

        #make search for request match in available requests
        match = difflib.get_close_matches(request_lower, requests_list_lower, n=n_matches, cutoff=accuray_matches)

        # if match: return single match or list of mupltiple matches, else: return None
        if len(match) == 1:
            return requests_list[requests_list_lower.index(match[0])]
        elif len(match) > 1:
            return match
        else:
            return None
    
    def _find_parameters_type_match(self, parameter_type, n_matches=1, accuracy_matches=0.4):
        ''' Finds closest match in available parameters types.
        '''
        #fix remove spaces and set all capital letters to lower
        parameter_type_lower = parameter_type.replace(' ','_')
        parameter_type_lower = parameter_type.lower()
        parameter_type_list = list(self.api_parameters.keys())
        parameter_type_list_lower = [each_string.lower() for each_string in parameter_type_list]

        #make search for request match in available parameter types
        match = difflib.get_close_matches(parameter_type_lower, parameter_type_list_lower, n=n_matches, cutoff=accuracy_matches)

        # if match: return single match or list of multiple matches, else: return None
        if len(match) == 1:
            return parameter_type_list[parameter_type_list_lower.index(match[0])] #return match from original list
        elif len(match) > 1:
            return match
        else:
            return None
    
    def _find_datetime_match(self, from_time, to_time=None): #TODO:
        ''' Find correct datetime from datetimeinput. If only from_time: return  and to time, returns datetimeinterval.
        Input: from_time (opt. to_time)
        Output: datetimestr (opt. datetimeintervalstr)
        '''
        
        #if datetime is datetime, return datetimestr
        if isinstance(datetime, datetime.datetime):
            #return datetimestr
            datetimestr = datetime.strftime(datetime, '%Y%m%d%H%M%S')
            return datetimestr
        
        #if datetime is string, check correct format
        #elif isinstance(datetime, str):
            #pass

    def find_parameters_match(self, parameter, parameter_type, n_matches=1, accuracy_matches=0.9):
        ''' 
        Finds closest match in available parameters.

        Input: parameter, parameter_type
        Output: matched_parameter_value, matched_parameter_code

        '''
        
        # Initially search for match on existance of spesified parameter type in entsoeapi.
        parameter_type_match = self._find_parameters_type_match(parameter_type=parameter_type)
        
        # If not found match on spesified parameter type.
        if parameter_type_match is None:

            # Return None.
            return None, None
        
        # Fix searchstring with removed spaces and all lowered letters.
        parameter_lower = parameter.replace(' ','_')
        parameter_lower = parameter.lower()
        
        # Store list of available parameter values in original and lowered form.
        parameter_values_list = list(self.api_parameters[parameter_type_match].values())
        parameter_values_list_lower = [each_string.lower() for each_string in parameter_values_list]
        
        # Store list of available parameter codes in original and lowered form.
        parameter_keys_list = list(self.api_parameters[parameter_type_match].keys())
        parameter_keys_list_lower = [each_string.lower() for each_string in parameter_keys_list]

        # Make search for match in parameter_values:
        match = difflib.get_close_matches(parameter_lower, parameter_values_list_lower, n=n_matches, cutoff=accuracy_matches)
        
        # If not loose match on string, check if whole parameter word in string
        # If not match in full string search.
        if len(match) < 1:

            # Loop on available parameters list,
            match = []
            for c in range(len(parameter_values_list_lower)):
                
                # Fix and split parameter values into list of substrings.
                b = parameter_values_list_lower[c].replace(",","")
                b = b.split(" ")

                # Search for match in list of parameter substrings.
                if parameter_lower in b:
                    
                    # If match is found, add to matchlist.
                    match.append(parameter_values_list_lower[c])
        
        # If match is found in parameter type values.
        if len(match) == 1:

            # Return matched value and code and parametertype.
            value = parameter_values_list[parameter_values_list_lower.index(match[0])]
            code = parameter_keys_list[parameter_values_list_lower.index(match[0])]
            return value, code
        
        # If not found match in values, search for match in keys:
        match = difflib.get_close_matches(parameter_lower, parameter_keys_list_lower, n=n_matches, cutoff=accuracy_matches)
            
        # If match is found in parameter type codes.
        if len(match) == 1:

            # Return matched value and code and parametertype
            value = parameter_values_list[parameter_keys_list_lower.index(match[0])]
            code = parameter_keys_list[parameter_keys_list_lower.index(match[0])]
            return value, code 

        # If no match found in either parameter type values or codes
        else:

            # Return None
            return None, None

    def _parse_xml_html_to_dict(self, response_xml_html, response_dict={}, level=0, level_location=['Response']):
        '''
        Recursive function for parsing xml- or html-response to response_dict.
        Input: response or html/xml textstring.
        Output: dict
        '''

        # If input is requests.Respons or raw string or r, create soup of input string:
        
        if isinstance(response_xml_html, str):
            response_xml_html = bs4.BeautifulSoup(response_xml_html, features="lxml")
        elif isinstance(response_xml_html, requests.Response):
            response_xml_html = bs4.BeautifulSoup(response_xml_html.text, features="lxml")

        # Loop through children.

        for child in response_xml_html.children:
        
            # Skip bastard children.

            if child.name == None or child.name == '\n':
                continue
            
            # If child has multiple descendants, increment level, walk down tree.

            if len(list(child.descendants)) > 1:
                level+=1
                level_location.append(child.name)
                response_dict, level_location  = self._parse_xml_html_to_dict(response_xml_html=child, response_dict=response_dict.copy(), level_location=level_location)
                level-=1
        
            # Else, store data as dict.

            else:
                key = tuple(level_location)

                # If not level_location in tuple, add as new.

                if key not in response_dict.keys():
                    response_dict[key] = [{child.name: child.contents[0]}]
                else:
                    response_dict[key].append({child.name: child.contents[0]})

        # If no more descendants on level, walk up level and decrement:

        if len(level_location) > 1:
            level_location.pop()
            return response_dict.copy(), level_location
    
        # If no more levels, create and return response_dict:

        lvl1_dict = {}
        for key, valuelist in response_dict.items():
            key1 = key[-1]
            lvl2_dict = {}
            for key2 in valuelist:
                key3 = list(key2.keys())[0]
                value3 = list(key2.values())[0]
                if key3 not in list(lvl2_dict.keys()):
                    lvl2_dict[key3] = [value3]
                else:
                    lvl2_dict[key3].append(value3)
            lvl1_dict[key1] =  lvl2_dict
        #if isinstance(lvl1_dict, tuple):
            #lvl1_dict[0] = lvl1_dict[0]
        return lvl1_dict.copy()
    


        # Parse soup_dict to muliindex_df?

        #series_list = []
        #for keys1, values1 in soup_dict.items():
        #
        #    #set column, run nested dict to store in lists.
        #    column=keys1[-1]
        #    index = []
        #    value = []
        #    for nest_dict in values1:
        #        for keys2, values2 in nest_dict.items():
        #            index.append(keys2)
        #            value.append(values2.string)
        #    series = pd.Series(data=value,index=index)
        #    series.name = column
        #    series_list.append(series)
        #
        ##create dict of series.
        #series_dict = {}
        #for a in series_list:
        #    series_dict[a.name] = a

        ##create multiseries.
        #multiseries = pd.concat(series_dict, axis=0)

        ##create multiindex df.
        #multidx_df = pd.DataFrame(multiseries)
        #multidx_df = multidx_df.rename(columns={0:'value'})

        #setattr(self, 'api_last_response_df', multidx_df)
        #return multidx_df




    #####################
    # Request call functions
    #####################
    @limits(calls=399, period=60) #max 400 calls pr minute or 10min ban..
    def _call_api(self, url=None, parameters_dict=None):
        '''Make call to api limited to , return full respons.
        '''
        # if url spesified, set url directly
        if url is not None:
            get_url = url
        # if parameters spesified, construct url
        elif parameters_dict is not None:
            get_url = self._construct_api_call_url(parameters_dict=parameters_dict)
        #if no url or parameters, cannot make call, return None.
        else:
            return None

        print(get_url)
        #makes request
        response = requests.get(get_url) 
        return response

        #return request respons
        #return None


    def _construct_api_call_url(self, parameters_dict, api_key=None, baseurl=None):
        '''Constructs api call url from baseurl, api_key and parameters_dict.
        '''
        #adds baseurl
        if baseurl is None:
            call_url = self.api_url
        else:
            call_url = baseurl
        
        #adds api_key
        if api_key is None:
            api_key = self.api_key
        call_url = call_url + 'securityToken=' + api_key
        
        #adds parameters
        for key, value in parameters_dict.items():
            call_url = call_url + '&' + key + '=' + value #syntax: &key=value 

        #return call_url
        return call_url



    #####################
    # Returner functions 
    #####################
    def return_show_available_requests(self, show_df=False, return_df=True):
        '''Show or return available requests as df.
        '''
        available_requests = pd.DataFrame(list(self.api_requests.keys()),columns=['Available requests'])
        if show_df:
            print(f'\nAvailable requests:\n{available_requests}')
        if return_df:
            return available_requests

    def return_show_available_parameter_types(self, show_df=False, return_df=True):
        '''Show or return available parameter types as df.
        '''
        available_param_types = pd.DataFrame(list(self.api_parameters.keys()),columns=['Available parameter types'])
        if show_df:
            print(f'Available parameter types:\n{available_param_types}')
        if return_df:
            return available_param_types

    def return_show_available_parameter(self, parameter_type,  show_dict=False, return_dict=True):
        '''Show or returns available parameter types as dict.
        '''
        #find match for parameter_type
        parameter_type_match = self._find_parameters_type_match(parameter_type=parameter_type, n_matches=1, accuracy_matches=0.4)
        
        # if match: shown. else: raise Exception
        if parameter_type_match in self.api_parameters.keys():
            available_params = self.api_parameters[parameter_type_match]
            available_params = available_params
            #available_params = pd.DataFrame.from_dict(self.api_parameters[parameter_type_match], orient='index')
            #available_params = available_params.transpose()
            #available_params = available_params.loc[0].to_dict()
            if show_dict:
                print(f'Available parameters for type "{parameter_type_match}":\n{available_params}')
            if return_dict:
                return available_params
        else:
            raise Exception (f'\nERROR: Found no match for your parameter type "{parameter_type}".\n Parameter type must resemble one in available api_parameters:\n {self.show_available_parameter_types()}')
    

#####################
# Main functions
#####################

def main():
    '''Main'''
    pass


if __name__ == "__main__":
    print("You called entsoeapi.py as __main__.")
    client = EntsoeClient(api_key='cdc4c0b1-7604-4270-9a85-77819dd8fea7')
    
    client.get_entsoe_statics_guide()
    #client.show_parameters()

    #client._get_entsoe_api_statics()

    #r = requests.get('https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html')

    #soup = bs4.BeautifulSoup(r.content)
    #print(soup.prettify())
    

