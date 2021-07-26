'''Contain module for parsing data from html/xml to dictionary.'''


import requests
import bs4
import pandas as pd

#response_success_key = 'response'
#response_error_key = 'error'


class SoupToDictClient():
    '''
    Structured HTML and XML may not be structured at all.
    This module walks through all tags the full html/xml tree, storing data in dictionary based on encounters found in tags while walking by.

    : Explained :

    - If encounter spesified in tag_to_key_dict is found, spesified key is added to dictionary.
    - While walking on, encounters spesified in tag_to_content_dict is stored as the key values in dictionary.
    - When new encounter spesified in tag_to_key_dict is found, new key is added to dictionary.
    - Walking on, new encounters spesified in tag_to_content_dict is stored as this key values.
    - And so, we walk on.


    '''

    def __init__(self):
        pass

    def get_parents_from_soup_ordered_list(self, soup):
        '''Return list of parents, tags with descendants, from soup.content'''

        # Create empty list to append parents with descendants.
        parents_list = []
            
        # Loop on soup contents.
        for content in soup.contents:

            # If content is parent with descendants.
            try:
                    
                 # Try if content has descendants.
                _ = content.descendants

                # Content is parent.
                parent = content

                # If list is empty
                if len(parents_list) == 0:

                    # Append parent to list of parents.
                    parents_list.append(parent)
                
                # else list is not empty.
                else:
                    
                    # If this parent has more descendants than the last parent in list.
                    if len(list(parent.descentands)) > len(list(parents_list[-1].descendants)):
                        
                        # Append this parent at end of list. 
                        parents_list.append(parent)
                    
                    # Else this parent has less descendants than last parent in list.
                    else:

                        # Add parent to list, before last parent in list.
                        parents_list.inser(-2, parent)

            # Else not parent with descendants
            except (AttributeError):
                
                # Do noting.
                None

        # If no parents found.
        if len(parents_list) == 0:

            # Return errormessage in dict and False flag.
            return {'message': 'No parent with descendants found in soup.content'}

        # Else parents found.
        else:

            # Return list of parents in soup successflagg
            return {'response': parents_list} 

    def _tag_tabular_to_df(self, table_tag, min_rows=2):
        '''Input a tag in a table, return the table as DataFrame'''
        
        # If parent is not a table_parent.
        if table_tag.name != 'table':

            # Set possible table_parent as table parent.
            table_tag = table_tag.find_parent('table')
        
        # If table parent has more than 1 row for table headers.
        if len(table_tag.find_all('tr')) >= min_rows:

            # Create list for storing rows.
            row_list = []

            # Find all rows.
            for row in table_tag.find_all('tr'): 

                # Create list for storing rows column values.
                row_col_list = []

                for row_col_value in row.find_all('td'):
                    row_col_list.append(row_col_value.text)

                row_list.append(row_col_list)
                            
            df = pd.DataFrame(row_list[1:], columns=row_list[0])
                            
            # Return dataframe as response.
            return df
        
        else:
            return None
    
    def _search_tag2dictkey_match(self, tag, keys_maplists, minmax_keylength = (2,500)):
        '''
        Inputs tag and spesified nested dictionary spesifying mappings to set dictionary key if matched.

        : Explains :
        - Input dictionary is mapped as: 
        - {"Matchset": {"Check if this tag attributes": {"Equals these contents": {"If so, then extract this tag attribute content as matched dict key"}}}
        - If multiple keys in all nested dicts within a matchset, checks for match in all combinations within the matchset.
        - If tag + att = cont in all layers within a matchset, tag + att + cont = matched key and returned as match.
        '''

        # Initially set tag2dictkey match to None.
        tag2dictkey = None

        # Loop on matchsets_lists in container list.
        for att_cont_att2key_keycont_matchsetlist in keys_maplists:
            
            # Loop on matchsets mapping spesified as tuples.
            for att_cont_attval_tuple in att_cont_att2key_keycont_matchsetlist:

                # If tag has spesified attribute.
                if hasattr(tag, att_cont_attval_tuple[0]):

                    # If spesified tag attribute equals to spesified content.
                    if getattr(tag, att_cont_attval_tuple[0]) == att_cont_attval_tuple[1] and att_cont_attval_tuple[2] or getattr(tag, att_cont_attval_tuple[0]) != att_cont_attval_tuple[1] and att_cont_attval_tuple[2] is False:

                        # Store attribute content spesified in key as key value.
                        keycont = getattr(tag, att_cont_attval_tuple[3])

                        if keycont is None:
                            keycont = ""

                        # If matched tag2dickkey is larger then spesified minimum.
                        if len(keycont) >= minmax_keylength[0] and len(keycont) <= minmax_keylength[1]:
                            
                            # Store the matched keyvalue of dict keyvalues.
                            tag2dictkey = keycont
                            
                        # If found non match in this set, set to None and break loop on set.
                        else:
                            tag2dictkey = None
                            break
                    else:
                        tag2dictkey = None
                        break
                else:
                    tag2dictkey = None
                    break

            # If match at end of a matchset.
            if tag2dictkey is not None:

                # Return match.
                return tag2dictkey
        
        # When done matchchecking all matchsets, return None or matched.
        return tag2dictkey

    def _has_attr(self, tag, att):
        '''Selfmade fix due to inconsistent response from hasattr()'''

        # Try to get tag attribute.
        try:
            resp = getattr(tag, att)
        # Except AttributeError, set resp to None.
        except(AttributeError, ValueError):
            resp = None

        # If response is not None, return True, else return False.
        if resp is not None:
            return True
        else:
            return False
    
    def _search_tag2dictcontent_key_value_match(self, tag, values_maplists):
        '''
        
        '''

        

        # Initially set matched key, value of main dicts value as a nested dict.
        contentkey = None
        contentvalue = None
        
        # Loop on the outer list, containing lists of searching matchsets.
        for att_cont_isBool_attIsValue_list in values_maplists:
            
            # Loop on each spesified tuple to match within a list of matchsets.
            for att_cont_isBool_attIsKey_tuple in att_cont_isBool_attIsValue_list:

                # Extract values in this search.
                spes_att = att_cont_isBool_attIsKey_tuple[0]
                spes_content = att_cont_isBool_attIsKey_tuple[1]
                spes_bool = att_cont_isBool_attIsKey_tuple[2]
                spes_asKey = att_cont_isBool_attIsKey_tuple[3]

                # Selfmade hasattr due to inconsintent hasattr() response.
                try:
                    has_attr = getattr(tag, spes_att)
                except(AttributeError, ValueError):
                    has_attr = False

                # If tag has search attribute spesified in the tuple.
                if self._has_attr(tag, spes_att):
                    
                    #if spes_att in list(tag.attrs.keys()):

                        #print(f"BLUE: {spes_att}")
                    

                    # If comparing tag attribute to tuple search content equals tuple search bool.
                    if getattr(tag, att_cont_isBool_attIsKey_tuple[0]) == att_cont_isBool_attIsKey_tuple[1] and att_cont_isBool_attIsKey_tuple[2]==True \
                        or getattr(tag, att_cont_isBool_attIsKey_tuple[0]) != att_cont_isBool_attIsKey_tuple[1] and att_cont_isBool_attIsKey_tuple[2] is False:
                        
                        
                        # If spesified contentkey is a tag attribute.
                        if self._has_attr(tag, att_cont_isBool_attIsKey_tuple[3]):

                            # Set contentvalue as content in tag attribute.
                            contentkey = att_cont_isBool_attIsKey_tuple[3]
                            contentvalue = getattr(tag, contentkey)
                            
                        # else if contentvalue is tabular.
                        elif att_cont_isBool_attIsKey_tuple[3].lower() in ['table', 'df', 'dataframe', 'tabular']:

                            # Try to make and store dataframe in contentvalue
                            try:
                                resp = self._tag_tabular_to_df(tag)

                                if resp is not None:
                                    contentkey = att_cont_isBool_attIsKey_tuple[3]
                                    contentvalue = resp
                                else:
                                    contentkey = None
                                    contentvalue = None
                                
                            # If not possible, store tag text as contentvalue.
                            except(AttributeError):
                                contentkey = att_cont_isBool_attIsKey_tuple[3]
                                contentvalue = tag.text

                        # Else, store tax text as contentvalue.
                        else:

                            # If content is not None.
                            if tag.text is not None:

                                # Set as content key, value
                                contentkey = att_cont_isBool_attIsKey_tuple[3]
                                contentvalue = tag.text



                    # If found non match in this set, set to None and break loop on set.
                    else:
                        contentkey = None
                        contentvalue = None
                        break
                else:
                    contentkey = None
                    contentvalue = None
                    break

            # If match at end of a matchset.
            if contentkey is not None:

                # Return match.
                return contentkey, contentvalue
        
        # When done matchchecking all matchsets, return None or matched.
        return contentkey, contentvalue


    def make_dict_from_soup(self, 
        soup_parent,  
        keys_maplists = [
            [('name', 'h2', True, 'string')],
            [('name', 'h3', True, 'string')],
            #[('name', 'h4', True, 'string')],
            [('name', 'p', True, 'string'), ('string', '1.4. Parameters', True, 'string')]],
            #'matchset3': {'name': {'h2': {'string': {}}}}},
            #'matchset4': {'string': {'1.4. Parameters': {'string': {}}}}},     
        values_maplists = [
            [('name', 'table', True, 'dataframe')]
            ],
        layer_counter=0,
        soup_dict={}
        ):
    
        '''
        Recursive function for parsing soup to dictionary.
        
        : Explains :
        - Walks through all tags in html/xml content.
        - Store content, based on encounters/flags spesified in tag_to_value_dict.
        - Mapping for encounters are: 
            containerlist:[
                match all tuples in this list: [
                    match all of me: ( 'tag attribute', is 'attribute content', equals 'True/False', return content in 'tag attribute' as dict key )]].

        - Adds the stored content as value to keys in dictionary, based on encounters/flags spesified in tag_to_key_dict.
    
        '''

        # 1. If this is first run, get parent from soup.
        if layer_counter <= 0:

            # If input soup_parent is not .
            if isinstance(soup_parent, bs4.BeautifulSoup) == False:

                # 
                if isinstance(soup_parent, str):

                    soup_parent = bs4.BeautifulSoup(soup_parent, features="lxml")

                    

                


            # Get list of parents from soup.
            parents_orderedlist_resp = self.get_parents_from_soup_ordered_list(soup=soup)

            if 'response' in parents_orderedlist_resp.keys():

                # Extract parent with most descendants from list.
                soup_parent = parents_orderedlist_resp[list(parents_orderedlist_resp.keys())[0]][-1]
            
            # Else no parents found in soup.
            else:

                # Return errormessage dict.
                return { 'message': 'No parents found in soup.'}

        # Increase layer_counter.
        layer_counter += 1
        
        # Walk down family tree.
        for child in soup_parent.children:

            #######################################
            ## Recursive function if descendants ##
            #######################################

            # If child has descendants, set child as parent and walk down recursive family tree.
            try:

                descendants = child.descendants
                
                # If child has multiple descendands.
                if int(len(list(child.descendants))) > 1:
                
                    # Put child as parent and recursively walk down tree.
                    soup_dict, layer_counter =  self.make_dict_from_soup(soup_parent=child, soup_dict=soup_dict, layer_counter=layer_counter, keys_maplists=keys_maplists, values_maplists=values_maplists)

                    # Decrease layer_counter.
                    layer_counter -= 1
            
            # Except.
            except (RuntimeError, TypeError, NameError, AttributeError):
                        
                # AttributeError: no descendants, do nothing.
                None
            
            ########################################
            ##  Search tag for match as dict key. ##
            ########################################

            # Search dict key matched to this tag.
            tag2dictkey = self._search_tag2dictkey_match(tag = child, keys_maplists=keys_maplists)
            
            # If found matched dict key.
            if tag2dictkey is not None:

                # Add key to dict, with value empty dict.
                soup_dict[tag2dictkey] = {}
            
            ##################################################
            ##  Search tag for match as dict value content. ##
            ##################################################
            
            contentkey, contentval = self._search_tag2dictcontent_key_value_match(tag=child, values_maplists=values_maplists)

            # If found content to store in tag.
            if contentkey is not None:
                
                # Extract the dict current last dict.
                key1 = list(soup_dict.keys())[-1]

                # If key is not in dictionary valuedict keys.
                if contentkey not in soup_dict[key1].keys():

                    # Add to dictionary as nested dict key, list.
                    soup_dict[key1][contentkey] = [contentval]

                # Else key exist in dictionary
                else:

                    # Append to contentlist at nested dict key.
                    soup_dict[key1][contentkey] = soup_dict[key1][contentkey].append(contentval)   
 
        #END for

        ############
        ## Return ##
        ############

        # If top layer and last child.
        if layer_counter <= 1 and child == list(soup_parent.children)[-1]:

            # Return finished soup_dict.
            return soup_dict

        # Else not finished
        else:

            # Return soup_dict and layer_counter to above tree layer.
            return soup_dict, layer_counter
        
        

                
        
        
        


if __name__ == "__main__":

    r = requests.get("https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html")

    soup = bs4.BeautifulSoup(r.text, features="lxml")
    
    #soup_ids = soup.find_all(id)
    #for ids in soup_ids:
    #    print(ids.string)
    client = SoupToDictClient()

    # Set mapping for choosing dict keys.
    soup_att_cont_isbool_setcontaskey_maplist = [
            [('name', 'h2', True, 'string')],
            [('name', 'h3', True, 'string')],
            [('name', 'h4', True, 'string')],
            [('name', 'p', True, 'string'), ('string', '1.4. Parameters', True, 'string')]
            ]

    # Set mapping for choosing dict values.
    soup_att_cont_isbool_setcontasvalue_maplist = [
            [('name', 'table', True, 'table')],
            [('name', 'code', True, 'code')],
            [('class', 'paragraph', True, 'paragraph'), ('text', '1.4 Parameters', False, 'paragraph')]
            #[('name', 'h4', True, 'string')],
            #[('name', 'p', True, 'string'), ('string', '1.4. Parameters', True, 'string')]
            ]



    soup_dict = client.make_dict_from_soup(soup, keys_maplists=soup_att_cont_isbool_setcontaskey_maplist, values_maplists=soup_att_cont_isbool_setcontasvalue_maplist)
    #print(soup_dict)
    print("OUT")
    
    for key, value in soup_dict.items():
        print(f'*{key}*')
        for key2, val2 in value.items():

            print(f"- {key2}")
            #print(val2)




    pass