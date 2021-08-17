
# Script for adding location coordinates to raw production-and-generation units datasets.

# Import libs.
import os
import pathlib
import pandas as pd
import glob

def merge_prod_gen_units_datasets(inputdirpath='', outputpath=''):
    '''Merges all raw production and generation unit datasets'''

    # Import libs.
    import pandas as pd
    import glob

    # Get path to data directory, get path to raw files directory, 
    # get list of filepaths in direcotry.
    datadirpath = pathlib.Path(__file__).parent.parent.joinpath('data')
    rawfilesdirpath = datadirpath.joinpath('raw//production-and-generation-units')
    rawfiles = glob.glob(f'{rawfilesdirpath}\\*.csv')

    # Create empty df
    df = pd.DataFrame()

    # Loop on files.
    for f in rawfiles:

        # Append files content to df.
        df = df.append(pd.read_csv(f, header=0))

    # Reset combined df index.
    df = df.reset_index(drop=True)

    return df

def decode_api_codes():
    ''''''


def create_geom_prod_gen_units_dataset(inputdirpath=''):
    '''Merge and coordinates to raw production and generation units datasets'''

    
    # If not spesified inputdirpath, set to default.
    if len(inputdirpath) <= 0 or inputdirpath is None:
        inputdirpath = pathlib.Path(__file__).parent.parent.joinpath('data//raw//production-and-generation-units')

    
    # Get all raw filepaths from directory.
    files = glob.glob(f'{inputdirpath}\\*.csv')

    # Create empty df
    df = pd.DataFrame()

    # Loop on files.
    for f in files:

        # Append files content to df.
        df = df.append(pd.read_csv(f, header=0))

    # Reset combined df index.
    df = df.reset_index(drop=True)

    

    return df


def main():
    '''Executing file as script.'''
    #create_geom_prod_gen_units_dataset()
    df = merge_prod_gen_units_datasets()
    print(df)


if __name__ == '__main__':
    main()