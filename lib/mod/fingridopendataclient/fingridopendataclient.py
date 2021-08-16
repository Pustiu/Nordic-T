# Import containerclass with static data for use of FingridApi services.
#from statics import FingridApiStatics

# Import libraries 
from ratelimit import limits
import datetime
import difflib
import requests
import pandas as pd

class FingridOpenDataClient():
    '''
    Pythonic Client Module, for interaction with the Fingrid Open Data-platforms API, and easy access to the platforms open datasets.
    Fingrid Open Data url: https://data.fingrid.fi/en/

    :How to use:
    - Request free api_key from the Fingrid Open Data platform, include in this module initialization.
    - Show list of available datasets using the function .show_available_datasets().
    - Extract datasets using the function .get_data(). Returns a dictionary containing the requested data responses.
    
    
    '''
    def __init__(self, api_key):

        # Statics
        self.static_datetimeformat_str = "%Y-%m-%dT%H:%M:%SZ"

        self.static_datasets_dict = self._datasets()

        self.static_datasets_names_list, self.static_datasets_variableids_list, self.static_datasets_formats_list, self.static_datasets_infos_list = self._datasets_values_to_lists()

        self.static_baseurl = 'https://api.fingrid.fi/v1'


        # Initialise inherance from all parent classes, setting fingridapi static data attributes.
        #super().__init__()

        # Store users api key.
        self.api_key = api_key

    
    ################################################################
    ############## Static Data.
    ################################################################

    def _datasets(self):
        '''Returns static data on of available api datasets as dict.'''
        return {
            'Other power transactions, down-regulation': {
                'VariableId': 213,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Other power transactions which are necessary in view of the power system.
                '''
            },
            'Other power transactions, up-regulation': {
                'VariableId': 214,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Other power transactions which are necessary in view of the power system.
                '''
            },
            'Fast Frequency Reserve FFR, procurement forecast': {
                'VariableId': 278,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The procurement prognosis for Fast Frequency Reserve (FFR) (MW). Fingrid procures FFR based on the procurement prognosis. The prognosis is updated once a day, typically at 11:00 (EET).

                The Fast Frequency Reserve (FFR) is procured to handle low-inertia situations. The needed volume of Fast Frequency Reserve depends on the amount of inertia in the power system and the size of the reference incident.
                '''
            },
            'Fast Frequency Reserve FFR, procured volume': {
                'VariableId': 276,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The volume of procured Fast Frequency Reserve (FFR). The procured volume will be published 22:00 (EET) on previous evening.

                The Fast Frequency Reserve (FFR) is procured to handle low-inertia situations. The needed volume of Fast Frequency Reserve depends on the amount of inertia in the power system and the size of the reference incident.
                '''
            },
            'Fast Frequency Reserve FFR, received bids': {
                'VariableId': 275,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The volume of received Fast Frequency Reserve (FFR) bids. The volume of bids will be published 22:00 (EET) on previous evening.

                The Fast Frequency Reserve (FFR) is procured to handle low-inertia situations. The needed volume of Fast Frequency Reserve depends on the amount of inertia in the power system and the size of the reference incident.
                '''
            },
            'Fast Frequency Reserve FFR, price': {
                'VariableId': 277,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The price of procured Fast Frequency Reserve (FFR) (€/MW). The price will be published 22:00 (EET) on previous evening. The price is determined by the price of the most expensive procured bid (marginal pricing).

                The Fast Frequency Reserve (FFR) is procured to handle low-inertia situations. The needed volume of Fast Frequency Reserve depends on the amount of inertia in the power system and the size of the reference incident.
                '''
            },
            'Kinetic energy of the Nordic power system - real time data': {
                'VariableId': 260,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Real-time estimate of the kinetic energy of the Nordic power system calculated by the Nordic transmission system operators.

                The data is updated every 1 minute.

                Historical data as of 2015/3/27 available.

                More information can be found on Fingrid's internet-site.
                '''
            },
            'Cross-border transmission fee, import from Russia': {
                'VariableId': 85,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Hourly cross-border transmission fee (dynamic tariff) for imports from Russia on Fingrid's connections.
                '''
            },
            'Cross-border transmission fee, export to Russia': {
                'VariableId': 86,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Hourly cross-border transmission fee (dynamic tariff) for exports to Russia on Fingrid's connections.
                '''
            },
            'Imbalance power between Finland and Sweden': {
                'VariableId': 	176,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The volume of power equals to the difference between measured and commercial transmission between Finland and Sweden. The tradetypes of commercial flow include day ahead, intraday and trades between Fingrid and Svenska Kraftnät during the operational hour. When the value of imbalance power volume is positive Fingrid has sold imbalance power to Sweden. When the value of imbalance power volume is negative Fingrid has bought imbalance power from Sweden.
                '''
            },
            'Emission factor of electricity production in Finland - real time data': {
                'VariableId': 	266,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Near in real time calculated carbon dioxide emission estimate of electricity production in Finland. The emissions are estimated by summing each product of different electricity production type and their emission factor together, and by dividing the sum by Finland's total electricity production.

                The data is updated every 3 minutes.
                '''
            },
            'Emission factor for electricity consumed in Finland - real time data': {
                'VariableId': 265,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Estimate of carbon dioxide of produced electricity, which is consumed in Finland. The emissions are estimated by taking FInland's electricity production, electricity import as well as electricity export into account.

                The data is updated every 3 minutes.
                '''
            },
            'Power system state - real time data': {
                'VariableId': 209,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Different states of the power system - traffic lights: 1=green, 2=yellow, 3=red, 4=black, 5=blue

                Green: Power system is in normal secure state.
                Yellow: Power system is in endangered state. The adequacy of the electricity is endangered or the power system doesn't fulfill the security standards.
                Red: Power system is in disturbed state. Load shedding has happened in order to keep the adequacy and security of the power system or there is a remarkable risk to a wide black out.
                Black: An extremely serious disturbance or a wide black out in Finland.
                Blue: The network is being restored after an extremely serious disturbance or a wide blackout.
                The data is updated every 3 minutes.
                '''
            },
            'Net import/export of electricity - real time data': {
                'VariableId': 	194,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Net import to Finland and net export from Finland. The data is updated every 3 minutes.

                Production information and import/export are based on the real-time measurements in Fingrid's operation control system.
                '''
            },
            'Transmission between Sweden and Åland - real time data': {
                'VariableId': 	90,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Power transmission between Åland and Sweden based on the real-time measurements in Fingrid's operation control system. Åland is a part of SE3 (Central-Sweden) bidding zone. Positive sign means transmission from Åland to Sweden. Negative sign means transmission from Sweden to Åland. The data is updated every 3 minutes.
                '''
            },
            'Transmission between Finland and Central Sweden - real time data': {
                'VariableId': 89,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Power transmission between Central Sweden (SE3) and Finland (FI) HVDC tie lines. Data is based on the real-time measurements in Fingrid's operation control system. Positive sign means transmission from Finland to Central Sweden (SE3). Negative sign means transmission from Central Sweden (SE3) to Finland. The data is updated every 3 minutes.
                '''
            },
            'Transmission between Finland and Norway - real time data': {
                'VariableId': 	187,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Power transmission between Finland and Norway 220kV AC tie line. Data is based on the real-time measurements in Fingrid's operation control system. Positive sign means transmission from Finland to Norway. Negative sign means transmission from Norway to Finland. The data is updated every 3 minutes.
                '''
            },
            'Transmission between Finland and Northern Sweden - real time data': {
                'VariableId': 	87,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Power transmission between Northern Sweden (SE1) and Finland (FI) 400kV AC tie line. Data is based on the real-time measurements in Fingrid's operation control system. Positive sign means transmission from Finland to Northern Sweden (SE1). Negative sign means transmission from Northern Sweden (SE1) to Finland. The data is updated every 3 minutes.
                '''
            },
            'Transmission between Finland and Russia - real time data': {
                'VariableId': 	195,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Power transmission between Finland and Russia based on the real-time measurements in Fingrid's operation control system. Positive sign means transmission from Finland to Russia. Negative sign means transmission from Russia to Finland. The data is updated every 3 minutes.
                '''
            },
            'Transmission between Finland and Estonia - real time data': {
                'VariableId': 	180,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Power transmission between Finland and Estonia HVDC tie lines (Estlink 1 and Estlink 2). Data is based on the real-time measurements in Fingrid's operation control system. Positive sign means transmission from Finland to Estonia. Negative sign means transmission from Estonia to Finland. The data is updated every 3 minutes.
                '''
            },
            'Balancing Capacity Market bids': {
                'VariableId': 	270,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The amount of bids in the balancing capacity market, MW/week. Fingrid procures mFRR capacity throught the balancing capacity market on a weekly auction, which is held when needed. Balance service provider pledges itself to leave regulating bids on the regulation market. For that the balance service provider is entitled to capacity payment. The amount of bids is published at latest on Friday on the week before the procurement week at 12:00 (EET)
                '''
            },
            'Balancing Capacity Market results': {
                'VariableId': 261,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The amount of capacity procured from the balancing capacity market, MW/week. Fingrid procures mFRR capacity throught the balancing capacity market on a weekly auction, which is held when needed. Balance service provider pledges itself to leave regulating bids on the regulation market. For that the balance service provider is entitled to capacity payment. The procured amount is published at latest on Friday on the week before the procurement week at 12:00 (EET)
                '''
            },
            'Frequency - historical data': {
                'VariableId': None,
                'Formats': ('zip'),
                'Info': 
                '''
                Frequency of the Nordic synchronous system with a 10 Hz sample rate.

                The frequency measurement data has been divided into archives consisting of monthly frequency measurement data. Within the archives, the data is divided into daily CSV-files that can be manipulated using common data analysis software.

                The frequency is measured at 400 kV substations at different locations in Finland with a sample rate of 10 Hz. The data may contain some gaps due to telecommunication errors etc. The times are according to UTC+2 / UTC+3 during daylight saving time period.
                '''
            },
            'Frequency - real time data': {
                'VariableId': 177,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Frequency of the power system based on the real-time measurements in Fingrid's operation control system. The data is updated every 3 minutes.
                '''
            },
            'Frequency containment reserve for disturbances, procured volumes in hourly market': {
                'VariableId': 82,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Hourly volume of procured frequency containment reserve for disturbances (FCR-D) in Finnish hourly market for each CET-timezone day is published previous evening at 22:45 (EET).

                FCR-D is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency above 49,5 Hz during disturbances.

                Hourly market is a reserve market operated by Fingrid. Procured volumes vary for each hour and price is the price of the most expensive procured bid.
                '''
            },
            'Frequency containment reserve for disturbances, received bids in hourly market': {
                'VariableId': 286,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The volume of received frequency containment reserve for disturbances (FCR-D) bids. The volume of bids will be published 22:45 (EET) on previous evening.

                FCR-D is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency above 49,5 Hz during disturbances.

                Hourly market is a reserve market operated by Fingrid. Procured volumes vary for each hour and price is the price of the most expensive procured bid.
                '''
            },
            'Frequency containment reserves for disturbances, hourly market prices': {
                'VariableId': 81,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Hourly prices (€/MW,h) of procured frequency containment reserve for disturbances (FCR-D) in Finnish hourly market for each CET-timezone day is published previous evening at 22:45 (EET).

                FCR-D is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency above 49,5 Hz during disturbances.

                Hourly market is a reserve market operated by Fingrid. Procured volumes vary for each hour and price is the price of the most expensive procured bid.
                '''
            },
            'Peak load power - real time data': {
                'VariableId': 183,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Activated peak load power based on the real-time measurements in Fingrid's operation control system including peak load reserve activations and trial runs during winter period. The data is updated every 3 minutes.
                '''
            },
            'Industrial cogeneration - real time data': {
                'VariableId': 202,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Cogeneration of industry based on the real-time measurements in Fingrid's operation control system. The data is updated every 3 minutes.

                Cogeneration means power plants that produce both electricity and district heating or process steam (combined heat and power, CHP).
                '''
            },
            'Hour change regulation, down-regulation': {
                'VariableId': 239,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                In order to reduce problems encountered at the turn of the hour in the Nordic countries or in Finland, the planned production changes will be transfered to begin 15 minutes before or after the planned moment.
                '''
            },
            'Hour change regulation, up-regulation': {
                'VariableId': 240,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                In order to reduce problems encountered at the turn of the hour in the Nordic countries or in Finland, the planned production changes will be transfered to begin 15 minutes before or after the planned moment.
                '''
            },
            'The sales price of production imbalance electricity': {
                'VariableId': 93,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The up-regulating price of the hour is the price of production imbalance power sold by Fingrid to a balance responsible party. If no up regulation has been made or if the hour has been defined as a down-regulation hour, the day ahead spot price of Finland is used as the selling price of production imbalance power. Prices are updated hourly.
                '''
            },
            'Surplus/deficit, cumulative - real time data': {
                'VariableId': 	186,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Information is based on the real time measurements in Fingrid's power control system.

                Power deficit/surplus represents the balance between production and consumption in Finland, taking into account imports and exports. It is calculated as the difference between the measured net import/export and the confirmed net exchange program between Finland and the other Nordic countries. The cumulative production deficit/surplus is the hourly energy generated from the difference.

                Sign convention: production deficit -, surplus +

                The data is updated every 3 minutes.
                '''
            },
            'Wind power production - real time data': {
                'VariableId': 	181,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Wind power production based on the real-time measurements in Fingrid's operation control system. About a tenth of the production capacity is estimated as measurements aren't available. The data is updated every 3 minutes.
                '''
            },
            'Wind power generation - hourly data': {
                'VariableId': 	75,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Finnish hourly wind power generation is a sum of measurements from wind parks supplied to Fingrid and of the estimate Fingrid makes from non-measured wind parks. Non-measured wind parks are about a tenth of the production capacity.
                '''
            },
            'Hydro power production - real time data': {
                'VariableId': 	191,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Hydro power production in Finland based on the real-time measurements in Fingrid's operation control system. The data is updated every 3 minutes.
                '''
            },
            'Nuclear power production - real time data': {
                'VariableId': 188,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Nuclear power production in Finland based on the real-time measurements in Fingrid's operation control system. The data is updated every 3 minutes.

                Due to the fire on our Olkiluoto substation the total amount of nuclear power measurement has been incorrect between 18 July at 09:00 to 20 July at 13:00. Data corrected 25.1.2019.
                '''
            },
            'Day-ahead transmission capacity SE1-FI – planned': {
                'VariableId': 142,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Planned day-ahead transmission capacity from North-Sweden (SE1) to Finland (FI). Transmission capacity is given hourly for every next week hour. Each week's hour is given one value. Planned weekly transmission capacity Fingrid will publish every Tuesday. Information will be updated if there are changes to the previous plan timetable or capacity. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Intraday transmission capacity FI - SE1': {
                'VariableId': 44,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Transmission capacity for intraday market from Finland to Northern Sweden (FI - SE1). For intraday market capacity is given as free capacity after dayahead market. Capacity is published once a day and not updated.
                '''
            },
            'Day-ahead transmission capacity FI-SE1 – planned': {
                'VariableId': 143,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Planned day-ahead transmission capacity from Finland (FI) to North-Sweden (SE1). Transmission capacity is given hourly for every next week hour. Each week's hour is given one value. Planned weekly transmission capacity Fingrid will publish every Tuesday. Information will be updated if there are changes to the previous plan timetable or capacity. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Intraday transmission capacity SE1-FI': {
                'VariableId': 38,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Transmission capacity for intraday market from Northern Sweden to Finland (SE1-FI). For intraday market capacity is given as free capacity after dayahead market. Capacity is published once a day and not updated.
                '''
            },
            'The sum of the down-regualtion bids in the Balancing energy market': {
                'VariableId': 	105,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The hourly sum of the down-regulation offers given by Finnish parties to the Balancing energy market is published hourly with one hour delay, eg. information from hour 07-08 is published at 9 o'clock.

                Balancing energy market is market place for manual freqeuncy restoration reserve (mFRR) which is used to balance the electricity generation and consumption in real time. The Balancing energy market organized by Fingrid is part of the Nordic Balancing energy market that is called also Regulating power market. Fingrid orders up- or down-regulation from the Balancing energy market. Down-regulation considers increasing of consumption or reducing of generation. Down-regulation bids have negative sign.
                '''
            },
            'The sum of the up-regulation bids in the balancing energy market': {
                'VariableId': 243,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The hourly sum of the up-regulation offers given by Finnish parties to the Balancing energy market is published hourly with one hour delay, eg. information from hour 07-08 is published at 9 o'clock.

                Balancing energy market is market place for manual freqeuncy restoration reserve (mFRR) which is used to balance the electricity generation and consumption in real time. The Balancing energy market organized by Fingrid is part of the Nordic Balancing energy market that is called also Regulating power market. Fingrid orders up- or down-regulation from the Balancing energy market. Up-regulation considers increasing of production or reducing of consumption.
                '''
            },
            'Day-ahead transmission capacity FI-SE3 – official': {
                'VariableId': 27,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Day-ahead transmission capacity from Finland (FI) to Central-Sweden (SE3). Transmission capacity is given hourly for every hour of the next day. Each hour is given one value. Day-ahead transmission capacity Fingrid will publish every day in the afternoon. This capacity will not changed after publication. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Transmission capacity RUS-FI': {
                'VariableId': 63,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The total commercial transmission capacity of the 400 kV transmission lines from Russia to Finland owned by Fingrid. The technical capacity on 400 kV lines from Russia to Finland is 1400 MW or 1000 MW, depending whether the NWPP power plant that is located in St. Petersburg area is connected to the Finnish or the Russian power system. Fingrid has reserved 100 MW of transmission capacity from Russia to Finland to buy reserve power. The technical maximum capacity from Finland to Russia is 350 MW, of which Fingrid has reserved 30 MW to buy reserve power.
                '''
            },
            'The buying price of production imbalance electricity': {
                'VariableId': 96,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The down-regulating price of the hour is the price of production imbalance power purchased by Fingrid from a balance responsible party. If no down-regulation has been made or if the hour has been defined as an up-regulation hour, the Elspot FIN price is used as the purchase price of production imbalance power.
                '''
            },
            'Intraday transmission capacity FI-EE – real time data': {
                'VariableId': 114,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Transmission capacity to be given to intraday market FI-EE. After Elspot trades have been closed, real time intraday capacity is equivalent to the allocated intraday capacity. The real time capacity is updated after each intraday trade so that it corresponds to real time situation.
                '''
            },
            'Commercial transmission of electricity between FI-SE3': {
                'VariableId': 32,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Commercial electricity flow (dayahead market and intraday market) between Finland (FI) and Central Sweden (SE3). Positive sign is export from Finland to Sweden.
                '''
            },
            'Bilateral trade capacity RUS-FI, unused': {
                'VariableId': 64,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Unused bilateral trade capacity From Russia (RUS) to Finland (FI). The capacity of electricity transmission in bilateral trade can be left unused if the parties do not import the maximum amount of electricity to Finland.
                '''
            },
            'Intraday transmission capacity FI-SE3': {
                'VariableId': 	45,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Transmission capacity for intraday market from Finland to Mid Sweden (FI - SE3). For intraday market capacity is given as free capacity after dayahead market. Capacity is published once a day and not updated.
                '''
            },
            'Day-ahead transmission capacity SE1-FI – official': {
                'VariableId': 	24,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Day-ahead transmission capacity from North-Sweden (SE1) to Finland (FI). Transmission capacity is given hourly for every hour of the next day. Each hour is given one value. Day-ahead transmission capacity Fingrid will publish every day in the afternoon. This capacity will not changed after publication. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Automatic Frequency Restoration Reserve, capacity, down': {
                'VariableId': 2,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Procured automatic Frequency Restoration Reserve (aFRR / FRR-A) capacity, down [MW]
                '''
            },
            'Automatic Frequency Restoration Reserve, activated, up': {
                'VariableId': 	54,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Activated automatic Frequency Restoration Reserve (aFRR) energy, up [MWh]
                '''
            },
            'Intraday transmission capacity SE3-FI': {
                'VariableId': 39,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Transmission capacity for intraday market from Mid Sweden to Finland (SE3-FI). Capacity for intraday market is given as free capacity after dayahead market. Capacity is published once a day and not updated.
                '''
            },
            'Electricity consumption forecast - updated hourly': {
                'VariableId': 166,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Electricity consumption forecast of Finland. The forecast is made by Fingrid and updated hourly.
                '''
            },
            'Electricity production, surplus/deficit - real time data': {
                'VariableId': 198,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Finland's energy production surplus/deficit. Information is based on the real time measurements in Fingrid's power control system.

                Power deficit/surplus represents the balance between power production and consumption in Finland, taking into account imports and exports. Power deficit/surplus is calculated as the difference between the measured net import/export and the confirmed net exchange program between Finland and the other Nordic countries.

                Sign convention: production deficit -, surplus +

                The data is updated every 3 minutes.
                '''
            },
            'Bilateral trade capacity FI-RUS, unused': {
                'VariableId': 49,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Unused bilateral trade capacity from Finland (FI) to Russia (RUS). The capacity of electricity transmission in bilateral trade can be left unused if the parties do not export the maximum amount of electricity to Russia.
                '''
            },
            'Transmission of electricity between Finland and Central Sweden - measured hourly data': {
                'VariableId': 61,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Measured electrical transmission between Finland and Central Sweden (SE3) high voltage direct current tie lines. Positive sign means transmission from Finland to Central Sweden (SE3). Negative sign means transmission from Central Sweden (SE3) to Finland.

                The value is updated once every hour after the hour shift. Each day before noon the values of the previous day are updated with more accurate measurement values.
                '''
            },
            'Commercial transmission of electricity between FI-SE1': {
                'VariableId': 31,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Commercial transmission of electricity (dayahead market and intraday market) between Finland (FI) and Northern Sweden (SE1). Positive sign is export from Finland to Sweden.
                '''
            },
            'Intraday transmission capacity FI-EE': {
                'VariableId': 113,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Transmission capacity to be given to intraday market FI-EE
                '''
            },
            'Intraday transmission capacity FI-RUS': {
                'VariableId': 	50,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The capacity given to intraday market means transfer capacity after day-ahead trade from Finland (FI) to Russia (RUS). The indraday capacity between Finland and Russia is updated once a day. The data will not be revised after hourly day-ahead trade.
                '''
            },
            'Measured transmission of electricity in Finland from north to south': {
                'VariableId': 30,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Measured electricity flow in North-South cut in Finland (cut P1). In the graph flow from North to South is positive.
                '''
            },
            'Day-ahead transmission capacity EE-FI – official': {
                'VariableId': 	112,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Day-ahead transmission capacity from Estonia (EE) to Finland (FI). Transmission capacity is given hourly for every hour of the next day. Each hour is given one value. Day-ahead transmission capacity Fingrid will publish every day in the afternoon. This capacity will not changed after publication. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Planned transmission capacity RUS-FI': {
                'VariableId': 127,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Planned transmission capacity from Russia to Finland. Transmission capacity is given hourly for every next week hour. Each week's hour is given one value. Planned weekly transmission capacity Fingrid will publish every Tuesday. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Planned transmission capacity FI-RUS': {
                'VariableId': 41,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Planned transmission capacity from Finland to Russia. Transmission capacity is given hourly for every next week hour. Each week's hour is given one value. Planned weekly transmission capacity Fingrid will publish every Tuesday. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Transmission of electricity between Finland and Estonia - measured hourly data': {
                'VariableId': 55,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Measured electrical transmission between Finland and Estonia HVDC tile lines (Estlink 1 and Estlink 2). Positive sign means transmission from Finland to Estonia. Negative sign means transmission from Estonia to Finland.

                The value is updated once every hour after the hour shift. Each day before noon the values of the previous day are updated with more accurate measurement values.
                '''
            },
            'Transmission capacity FI-RUS': {
                'VariableId': 103,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                The total commercial transmission capacity of the 400 kV transmission lines from Finland to Russia owned by Fingrid. The technical capacity on 400 kV lines from Russia to Finland is 1400 MW or 1000 MW, depending whether the NWPP power plant that is located in St. Petersburg area is connected to the Finnish or the Russian power system. Fingrid has reserved 100 MW of transmission capacity from Russia to Finland to buy reserve power. The technical maximum capacity from Finland to Russia is 350 MW, of which Fingrid has reserved 30 MW to buy reserve power.
                '''
            },
            'Planned weekly capacity from south to north': {
                'VariableId': 	29,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Planned weekly capacity on North-South cut in Finland (cut P1) from South to North. Planned outages are included in the weekly capacity, information is not updated after disturbances.
                '''
            },
            'Intraday transmission capacity EE-FI': {
                'VariableId': 110,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Transmission capacity to be given to intraday market EE - FI
                '''
            },
            'Wind power generation forecast - updated once a day': {
                'VariableId': 246,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Finnish wind power generation forecasts for the next day. Forecast is updated every day at 12 p.m. EET. Length of the forecast is 36 hours. Overlapping hours are overwritten.

                The forecast is based on weather forecasts and data about the location, size and capacity of wind turbines. The weather data sourced from multiple providers.
                '''
            },
            'Day-ahead transmission capacity FI-EE – official': {
                'VariableId': 	115,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Day-ahead transmission capacity from Finland (FI) to Estonia (EE). Transmission capacity is given hourly for every hour of the next day. Each hour is given one value. Day-ahead transmission capacity Fingrid will publish every day in the afternoon. This capacity will not changed after publication. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Total production capacity used in the solar power forecast': {
                'VariableId': 267,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                This is the total solar power production capacity used in Fingrid's solar power forecast. It is based on the small scale production statistics gathered by the Energy authority. It is also updated with estimates based on information that's provided to Fingrid.

                This total capacity information can be used, for example, to calculate the rate of production of solar power, by comparing it to the forecasted solar production series by Fingrid. This capacity information cannot however be considered as the official amount of solar production capacity in Finland, as it is updated manually and by using estimates.
                '''
            },
            'Wind power generation forecast - updated hourly': {
                'VariableId': 245,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Finnish wind power generation forecast for the next 36 hours. Updated hourly.

                The forecast is based on weather forecasts and data about the location, size and capacity of wind turbines. The weather data sourced from multiple providers.
                '''
            },
            'Electricity consumption forecast - next 24 hours': {
                'VariableId': 165,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                An hourly consumption forecast for the next 24 hours made by Fingrid. Forecast is published on previous day at 12:00 EET.
                '''
            },
            'Electricity consumption in Finland': {
                'VariableId': 124,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Electricity consumption in Finland is based on Fingrid's production measurements. Minor part of production which is not measured is estimated. The consumption is calculated as follows: Consumption = Production + Import - Export. Updated hourly.
                '''
            },
            'Bilateral trade between FI-RUS': {
                'VariableId': 	68,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Bilateral trade between Finland and Russia. Fingrid and the Russian parties confirm the bilateral trades on 400 kV cross-border connection in the morning of the commercial day D for the following commercial day D+1. The confirmed bilateral trades will be bid price-independently on the electricity spot market
                '''
            },
            'Condensing power production - real time data': {
                'VariableId': 	189,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Condensing power production based on the real-time measurements in Fingrid's operation control system. The data is updated every 3 minutes.

                Publishing this data has been stopped since 14.9.2017 due to changes in division of power plants. The production data is included in other real time production measurement time series.
                '''
            },
            'Intraday transmission capacity EE-FI – real time data': {
                'VariableId': 	111,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Transmission capacity to be given to intraday market EE-FI. After Elspot trades have been closed, real time intraday capacity is equivalent to the allocated intraday capacity. The real time capacity is updated after each intraday trade so that it corresponds to real time situation.
                '''
            },
            'Ordered down-regulations from Balancing energy market in Finland': {
                'VariableId': 	33,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Ordered down-regulations from Balancing energy market in Finland. The volume of ordered down-regulations from Balancing energy market in Finland is published hourly with two hours delay, eg. information from hour 06-07 is published at 9 o'clock.

                Balancing energy market is market place for manual freqeuncy restoration reserve (mFRR) which is used to balance the electricity generation and consumption in real time. The Balancing energy market organized by Fingrid is part of the Nordic Balancing energy market that is called also Regulating power market. Fingrid orders up- or down-regulation from the Balancing energy market. Down-regulation considers increasing of consumption or reducing of generation. Down-regulation volume has negative sign.
                '''
            },
            'Electricity consumption in Finland - real time data': {
                'VariableId': 	193,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Electricity consumption in Finland is calculated based on production and import/export. The data is updated every 3 minutes.

                Production information and import/export are based on the real-time measurements in Fingrid's operation control system.
                '''
            },
            'Temperature in Jyväskylä - real time data': {
                'VariableId': 182,
                'Formats': ('csv', 'json', 'app'),
                'Info':
                '''
                Outside air temperature measurement at Petäjävesi substation. The data is updated every 3 minutes.
                '''
            },
            'Cogeneration of district heating - real time data': {
                'VariableId': 201,
                'Formats': ('csv', 'json', 'app'),
                'Info':
                '''
                Cogeneration of district heating based on the real-time measurements in Fingrid's operation control system. The data is updated every 3 minutes.

                Cogeneration means power plants that produce both electricity and district heating or process steam (combined heat and power, CHP).
                '''
            },
            'Special regulation, up-regulation': {
                'VariableId': 119,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                ​Regulation which takes place in the regulating power market by Fingrid for reasons other than the needs of national balance management
                '''
            },
            'Temperature in Helsinki - real time data': {
                'VariableId': 178,
                'Formats': ('csv', 'json', 'app'),
                'Info':
                '''
                Outside air temperature measurement at Tammisto substation. The data is updated every 3 minutes.
                '''
            },
            'Electricity production in Finland - real time data': {
                'VariableId': 192,
                'Formats': ('csv', 'json', 'app'),
                'Info':
                '''
                Electricity production in Finland based on the real-time measurements in Fingrid's operation control system The data is updated every 3 minutes.
                '''
            },
            'Automatic Frequency Restoration Reserve, price, up': {
                'VariableId': 52,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Volume weighted average price for procured upward automatic Frequency Restoration Reserve (aFRR) capacity, [€/MW]
                '''
            },
            'Automatic Frequency Restoration Reserve, price, down': {
                'VariableId': 	51,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Volume weighted average price for procured downward automatic Frequency Restoration Reserve (aFRR) capacity, [€/MW]
                '''
            },
            'Time deviation - real time data': {
                'VariableId': 	206,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Time deviation is the time difference in seconds between a clock running according to the frequency of the grid and a reference clock independent of the frequency of the grid. The data is updated every 3 minutes.
                '''
            },
            'Stock exchange trade FI-RUS-FI': {
                'VariableId': 	69,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Direct trade volumes derive from freely placed bids in the Nordic day-ahead (Elspot) and intraday (Elbas) electricity markets. Information is updated once the day-ahead market results are public. Information on the intraday trade is updated before the operational hour.
                '''
            },
            'Electricity production prediction - updated hourly': {
                'VariableId': 241,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The calculation of production forecast in Finland is based on the production plans that balance responsible parties has reported to Fingrid. Production forecast is updated hourly.
                '''
            },
            'Automatic Frequency Restoration Reserve, capacity, up': {
                'VariableId': 	1,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Procured automatic Frequency Restoration Reserve (aFRR) capacity, up [MW]
                '''
            },
            'Transmission of electricity between Finland and Northern Sweden - measured hourly data': {
                'VariableId': 60,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Measured transmission of electricity between Finland and Northern Sweden (SE1). Positive sign means transmission from Finland to Northern Sweden (SE1). Negative sign means transmission from Northern Sweden (SE1) to Finland.

                The value is updated once every hour after the hour shift. Each day before noon the values of the previous day are updated with more accurate measurement values.
                '''
            },
            'Temperature in Oulu - real time data': {
                'VariableId': 196,
                'Formats': ('csv', 'json', 'app'),
                'Info': 
                '''
                Outside air temperature measurement at Leväsuo substation. The data is updated every 3 minutes.
                '''
            },
            'Total production capacity used in the wind power forecast': {
                'VariableId': 268,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                This is the total wind production capacity used in Fingrid's wind power forecast. It is based capacity information gathered by Fingrid.

                This total capacity information can be used, for example, to calculate the rate of production of wind power, by comparing it to the actual wind production series by Fingrid. This capacity information cannot however be considered as the official amount of wind production capacity in Finland, as it is updated manually.
                '''
            },
            'Temperature in Rovaniemi - real time data': {
                'VariableId': 	185,
                'Formats': ('csv', 'json', 'app'),
                'Info':
                '''
                Outside air temperature measurement at Valajaskoski substation. The data is updated every 3 minutes.
                '''
            },
            'Stock exchange capacity FI-RUS': {
                'VariableId': 	102,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The capacity on the 400 kV connection from Finland to Russia is reserved to direct trade of the following commercial day. Fingrid and the Russian parties, who have jointly agreed that the capacity is 140 MW in both directions, daily confirm the capacity.
                '''
            },
            'Transmission of electricity between Finland and Russia - measured hourly data': {
                'VariableId': 	58,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Measured electrical transmission between Finland and Russia. Positive sign means transmission from Finland to Russia. Negative sign means transmission from Russia to Finland.

                The value is updated once every hour after the hour shift. Each day before noon the values of the previous day are updated with more accurate measurement values.
                '''
            },
            'Electricity production prediction - premilinary': {
                'VariableId': 242,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Hourly electricity generation forecast is based on the production plans that balance responsible parties have reported to Fingrid. The forecast is published daily by 6.00 pm for the next day, and it is not updated to match the updated production plans that balance responsible parties send to Fingrid hourly.
                '''
            },
            'Automatic Frequency Restoration Reserve, activated, down': {
                'VariableId': 53,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Activated automatic Frequency Restoration Reserve (aFRR) energy, down [MWh]
                '''
            },
            'The price of comsumption imbalance electricity': {
                'VariableId': 	92,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The price of consumption imbalance power is the price for which Fingrid both purchases imbalance power from a balance responsible party and sells it to one. In the case of regulating hour, the regulation price is used. If no regulation has been made, the Elspot FIN price is used as the purchase and selling price of consumption imbalance power. Data gathering to Excel-sheet or XML format is possible in periods not longer that one year due to limitations in data transmission.
                '''
            },
            'Electricity production in Finland': {
                'VariableId': 	74,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Hourly electricity production in Finland are based on Fingrid's measurements. Minor part of production which is not measured is estimated. Updated hourly.
                '''
            },
            'Commercial transmission of electricity between FI-EE': {
                'VariableId': 	140,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Commercial electricity flow (dayahead market and intraday market) between Finland (FI) and Estonia (EE) including system supportive trade between TSOs. Positive sign is export from Finland to Estonia.
                '''
            },
            'Transmission of electricity between Finland and Norway - measured hourly data': {
                'VariableId': 	57,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Measured electrical transmission between Finland and Norway 220kV tie line. Positive sign means transmission from Finland to Norway. Negative sign means transmission from Norway to Finland.

                The value is updated once every hour after the hour shift. Each day before noon the values of the previous day are updated with more accurate measurement values.
                '''
            },
            'Special regulation, down-regulation': {
                'VariableId': 118,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Regulation which takes place in the regulating power market by Fingrid for reasons other than the needs of national balance management
                '''
            },
            'Electricity production, reserve power plants and small-scale production - real time data': {
                'VariableId': 205,
                'Formats': ('csv', 'json', 'app'),
                'Info':
                '''
                Reserve power plants electrical production is based on the real-time measurements in Fingrid's operation control system. Estimated small-scale production is added, of which there are no measurements available. The data is updated every 3 minutes.
                '''
            },
            'Frequency Containment Reserve for Normal operation, hourly market bids': {
                'VariableId': 285,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The volume of received Frequency Containment Reserves for Normal operation (FCR-N) bids. The volume of bids will be published 22:45 (EET) on previous evening.

                FCR-N is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency in normal frequency range between 49,9 - 50,1 Hz.

                Hourly market is a reserve market operated by Fingrid. Procured volumes vary for each hour and price is the price of the most expensive procured bid.
                '''
            },
            'Frequency Containment Reserve for Normal operation, activated': {
                'VariableId': 123,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Activated Frequency Containment Reserve for Normal operation (FCR-N) is published hourly one hour after the hour in question, for example the value for hour 07-08 is published at 9 o'clock.

                FCR-N is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency in normal frequency range between 49,9 - 50,1 Hz.

                Activated FCR-N volume (MWh) is calculated on the basis of the frequency in the Nordic synchronous system.

                Value is activated net energy. Positive value means that the frequency has been in average below 50,0 Hz during the hour, and reserve has been activated as up-regulation. Respectively, negative value means that the frequency has been in average above 50,0 Hz, and reserve has been activated as down-regulation.
                '''
            },
            'Bilateral trade capacity FI-RUS': {
                'VariableId': 	101,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The bilateral capacity on the 400 kV connection from Russia to Finland that is reserved to bilateral trade of the following commercial day. The capacity is confirmed by Fingrid and the Russian parties.
                '''
            },
            'Transmission of electricity between Finland and Åland - measured hourly data': {
                'VariableId': 280,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Measured electrical transmission between Finland and Åland islands DC tie line. Positive sign means transmission from Finland to Åland. Negative sign means transmission from Åland to Finland.

                The value is updated once a day before noon with the values of the previous day.
                '''
            },
            'Activated down-regulation power': {
                'VariableId': 	252,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The activated downward power from balancing power market. The value is given for each 15 minutes and indicated the amount of activated power in the end of each 15 minute time period. The values are available starting from December 2018.
                '''
            },
            'Ordered up-regulations from Balancing energy market in Finland': {
                'VariableId': 	34,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Ordered up-regulations from Balancing energy market in Finland. The volume of ordered up-regulations from Balancing energy market in Finland is published hourly with two hours delay, eg. information from hour 06-07 is published at 9 o'clock.

                Balancing energy market is market place for manual freqeuncy restoration reserve (mFRR) which is used to balance the electricity generation and consumption in real time. The Balancing energy market organized by Fingrid is part of the Nordic Balancing energy market that is called also Regulating power market. Fingrid orders up- or down-regulation from the Balancing energy market. Up-regulation considers increasing of generation or reducing of consumption.
                '''
            },
            'Stock exchange capacity RUS-FI': {
                'VariableId': 67,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The capacity on the 400 kV connection from Russia to Finland is reserved to direct trade of the following commercial day. Fingrid and the Russian parties, who have jointly agreed that the capacity is 140 MW in both directions, daily confirm the capacity.
                '''
            },
            'Day-ahead transmission capacity FI-SE3 – planned': {
                'VariableId': 145,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Planned day-ahead transmission capacity from Finland (FI) to Central-Sweden (SE3). Transmission capacity is given hourly for every next week hour. Each week's hour is given one value. Planned weekly transmission capacity Fingrid will publish every Tuesday. Information will be updated if there are changes to the previous plan timetable or capacity. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Solar power generation forecast - updated once a day': {
                'VariableId': 	247,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Solar power generation forecasts for the next day. Forecast is updated every day at 12 p.m. EET. Length of the forecast is 36 hours. Overlapping hours are overwrited.

                Solar forecasts are based on weather forecasts and estimates of installed PV capacity and location in Finland. Total PV capacity is based on yearly capacity statistics from the Finnish energy authority and estimates on installation rate of new capacity. Location information is a very rough estimate based on Finnish distribution grid operators information.
                '''
            },
            'Frequency Containment Reserve for Normal operation, hourly market volumes': {
                'VariableId': 80,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Hourly volume of procured frequency containment reserve for normal operation (FCR-N) in Finnish hourly market for each CET-timezone day is published previous evening at 22:45 (EET).

                FCR-N is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency in normal frequency range between 49,9 - 50,1 Hz.

                Hourly market is a reserve market operated by Fingrid. Procured volumes vary for each hour and price is the price of the most expensive procured bid.
                '''
            },
            'Bilateral trade capacity RUS-FI': {
                'VariableId': 	65,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The bilateral capacity on the 400 kV connection from Russia (RUS) to Finland (FI) that is reserved to bilateral trade of the following commercial day. The capacity is confirmed by Fingrid and the Russian parties.
                '''
            },
            'Congestion income between FI-SE3': {
                'VariableId': 	71,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Congestion income between Finland (FI) and Central Sweden (SE3).

                Congestion income is published on ENTSO-E's Transparency Platform, which can be founded here: https://transparency.entsoe.eu/transmission/r2/dailyImplicitAllocationsCongestionIncome/show . There are historical values to be found from Open Data until the beginning of February 2017. After February 2017 updated data as well as historical data can be founded from ENTSO-E's Transparency Platform.

                Congestion income = commercial flow between FI and SE3 on the day ahead market [MWh/h] * absolute value of price difference between FI and SE3 [€/MWh].

                Congestion originates in the situation where transmission capacity between bidding zones is not sufficient to fulfill the market demand and the congestion splits the bidding zones into separate price areas. Congestion income arises from the different prices that the sellers receive and the buyers pay when electricity flows from the higher price area to the lower price area. The seller acting in a lower price area receives lower price for electricity compared to the price the other party pays for electricity in the higher price area, and the power exchange receives surplus income, which it then pays to the Transmission System Operators (TSOs). The TSOs spend the received congestion income on increasing the transmission capacity on its cross-border interconnectors according to the EU regulation.
                '''
            },
            'Activated up-regulation power': {
                'VariableId': 	253,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The activated upward power from balancing power market. The value is given for each 15 minutes and indicated the amount of activated power in the end of each 15 minute time period. The values are available starting from December 2018.
                '''
            },
            'Day-ahead transmission capacity SE3-FI – planned': {
                'VariableId': 	144,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Planned day-ahead transmission capacity from Central-Sweden (SE3) to Finland (FI). Transmission capacity is given hourly for every next week hour. Each week's hour is given one value. Planned weekly transmission capacity Fingrid will publish every Tuesday. Information will be updated if there are changes to the previous plan timetable or capacity. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Solar power generation forecast - updated hourly': {
                'VariableId': 248,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Hourly updated solar power generation forecast for the next 36 hours.

                Solar forecasts are based on weather forecasts and estimates of installed PV capacity and location in Finland. Total PV capacity is based on yearly capacity statistics from the Finnish energy authority and estimates on installation rate of new capacity. Location information is a very rough estimate based on Finnish distribution grid operators information.
                '''
            },
            'Frequency Containment Reserve for Normal operation, hourly market prices': {
                'VariableId': 79,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Hourly prices (€/MW,h) of procured frequency containment reserve for normal operation (FCR-N) in Finnish hourly market for each CET-timezone day is published previous evening at 22:45 (EET).

                FCR-N is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency in normal frequency range between 49,9 - 50,1 Hz.

                Hourly market is a reserve market operated by Fingrid. Procured volumes vary for each hour and price is the price of the most expensive procured bid.
                '''
            },
            'Frequency containment reserves for disturbances, nordic trade': {
                'VariableId': 	289,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The volume of the nordic trade of frequency containment reserve for disturbances (FCR-D) capacity. Positive numbers indicate import of capacity to Finland and negative numbers indicate export of capacity from Finland. The data contains the traded capacity for Sweden and Norway. The data will be published 22:45 (EET) on previous evening.

                FCR-D is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency above 49,5 Hz during disturbances.

                Hourly market is a reserve market operated by Fingrid. Procured volumes vary for each hour and price is the price of the most expensive procured bid.
                '''
            },
            'Price of the last activated up-regulation bid - real time data': {
                'VariableId': 	22,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The price of the last activated up-regulation bid. The price is published real-time when Finland is a separate regulation area.
                '''
            },
            'Congestion income between FI-EE': {
                'VariableId': 48,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Congestion income between Finland (FI) and Estonia (EE).

                Congestion income is published on ENTSO-E's Transparency Platform, which can be founded here: https://transparency.entsoe.eu/transmission/r2/dailyImplicitAllocationsCongestionIncome/show . There are historical values to be found from Open Data until the beginning of February 2017. After February 2017 updated data as well as historical data can be founded from ENTSO-E's Transparency Platform.

                Congestion income is calculated as follows: congestion income [€/h] = commercial flow on day ahead market [MW] * area price difference [€/MWh]

                Congestion originates in the situation where transmission capacity between bidding zones is not sufficient to fulfill the market demand and the congestion splits the bidding zones into separate price areas. Congestion income arises from the different prices that the sellers receive and the buyers pay when electricity flows from the higher price area to the lower price area. The power exchange receives the difference, which it then pays to the Transmission System Operators (TSOs). The TSOs spend the received congestion income on increasing the transmission capacity on its cross-border interconnectors according to the EU regulation.
                '''
            },
            'Intraday transmission capacity RUS-FI': {
                'VariableId': 	66,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The capacity given to intraday market means transfer capacity after day-ahead trade from Russia to Finland. The intraday capacity between Finland and Russia is updated once a day. The data will not be revised after hourly day-ahead trade.
                '''
            },
            'Down-regulation bids, price of the last activated - real time data': {
                'VariableId': 251,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The price of the last activated down-regulation bid. The price is published real-time when Finland is a separate regulation area.
                '''
            },
            'Down-regulation price in the Balancing energy market': {
                'VariableId': 106,
                'Formats': ('csv', 'json'),
                'Info': 
                '''
                Down-regulation price in the Balancing energy market. The price of the cheapest regulating bid used in the balancing power market during the particular hour; however, at the most the price for price area Finland in Nord Pool Spot (Elspot FIN).

                Down-regulating price in Finland is the price of the most expensive down-regulating bid used in the Balancing energy market during the hour in question; however, it is at the most the day ahead market price for the price area Finland. Down-regulating price for each hour is published hourly with one hour delay, eg. information from hour 07-08 is published at 9 o'clock.

                Balancing energy market is market place for manual freqeuency restoration reserve (mFRR) which is used to balance the electricity generation and consumption in real time. The Balancing energy market organized by Fingrid is part of the Nordic Balancing energy market that is called also Regulating power market. Fingrid orders up- or down-regulation from the Balancing energy market. Down-regulation considers increasing of consumption or reducing of generation.
                '''
            },
            'Congestion income between FI-SE1': {
                'VariableId': 70,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Congestion income between Finland (FI) and Northern Sweden (SE1).

                Congestion income is published on ENTSO-E's Transparency Platform, which can be founded here: https://transparency.entsoe.eu/transmission/r2/dailyImplicitAllocationsCongestionIncome/show . There are historical values to be found from Open Data until the beginning of February 2017. After February 2017 updated data as well as historical data can be founded from ENTSO-E's Transparency Platform.

                Congestion income is calculated as follows: congestion income [€/h] = commercial flow on day ahead market [MW] * area price difference [€/MWh]

                Congestion originates in the situation where transmission capacity between bidding zones is not sufficient to fulfill the market demand and the congestion splits the bidding zones into separate price areas. Congestion income arises from the different prices that the sellers receive and the buyers pay when electricity flows from the higher price area to the lower price area. The seller acting in a lower price area receives lower price for electricity compared to the price the other party pays for electricity in the higher price area, and the power exchange receives surplus income, which it then pays to the Transmission System Operators (TSOs). The TSOs spend the received congestion income on increasing the transmission capacity on its cross-border interconnectors according to the EU regulation.
                '''
            },
            'Planned weekly capacity from north to south': {
                'VariableId': 28,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Planned weekly capacity on North-South cut in Finland (cut P1) from North to South. Planned outages are included in the weekly capacity, information is not updated after disturbances.
                '''
            },
            'Day-ahead transmission capacity FI-SE1 – official': {
                'VariableId': 26,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Day-ahead transmission capacity from Finland (FI) to North-Sweden (SE1). Transmission capacity is given hourly for every hour of the next day. Each hour is given one value. Day-ahead transmission capacity Fingrid will publish every day in the afternoon. This capacity will not changed after publication. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Day-ahead transmission capacity SE3-FI – official': {
                'VariableId': 25,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Day-ahead transmission capacity from Central-Sweden (SE3) to Finland (FI). Transmission capacity is given hourly for every hour of the next day. Each hour is given one value. Day-ahead transmission capacity Fingrid will publish every day in the afternoon. This capacity will not changed after publication. Transmission capacity mean the capability of the electricity system to supply electricity to the market without compromising the system security.
                '''
            },
            'Frequency Containment Reserve for Normal operation, foreign trade': {
                'VariableId': 287,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The volume of the foreign trade of frequency containment reserve for normal operation (FCR-N) capacity. Positive numbers indicate import of capacity to Finland and negative numbers indicate export of capacity from Finland. The data contains the traded capacity for Sweden, Norway, Estonia and Russia. The data will be published 22:45 (EET) on previous evening.

                FCR-N is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency in normal frequency range between 49,9 - 50,1 Hz.

                Hourly market is a reserve market operated by Fingrid. Procured volumes vary for each hour and price is the price of the most expensive procured bid.
                '''
            },
            'Up-regulating price in the Balancing energy market': {
                'VariableId': 244,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                Up-regulating price in Finland is the price of the most expensive up-regulating bid used in the Balancing energy market during the hour in question; however, it is at least the day ahead market price for the price area Finland. Up-regulating price for each hour is published hourly with one hour delay, eg. information from hour 07-08 is published at 9 o'clock.

                Balancing energy market is market place for manual freqeuncy restoration reserve (mFRR) which is used to balance the electricity generation and consumption in real time. The Balancing energy market organized by Fingrid is part of the Nordic Balancing energy market that is called also Regulating power market. Fingrid orders up- or down-regulation from the Balancing energy market. Up-regulation considers increasing of production or reducing of consumption.
                '''
            },
            'Balancing Capacity Market price': {
                'VariableId': 262,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The price of capacity procured from the balancing capacity market, €/MW,h. Fingrid procures mFRR capacity throught the balancing capacity market on a weekly auction, which is held when needed. Balance service provider pledges itself to leave regulating bids on the regulation market. For that the balance service provider is entitled to capacity payment. The price is published at latest on Friday on the week before the procurement week at 12:00 (EET)
                '''
            },
            'Frequency containment reserves for disturbances, reserve plans in the yearly market': {
                'VariableId': 	290,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The hourly sum of reserve plans for frequency containment reserve for disturbances (FCR-D) in the yearly market. The data will be published 22:45 (EET) on previous evening.

                FCR-D is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency above 49,5 Hz during disturbances.

                Yearly market is a reserve market operated by Fingrid. Hourly procured volumes vary according to the reserve plans submitted by the balancing service providers and the price is constant over the whole year.
                '''
            },
            'Frequency Containment Reserve for Normal operation, yearly market plans': {
                'VariableId': 288,
                'Formats': ('csv', 'json'),
                'Info':
                '''
                The hourly sum of reserve plans for frequency containment reserve for normal operation (FCR-N) in the yearly market. The data will be published 22:45 (EET) on previous evening.

                FCR-N is the frequency containment reserve used in the Nordic synchronous system that aims to keep the frequency in normal frequency range between 49,9 - 50,1 Hz.

                Yearly market is a reserve market operated by Fingrid. Hourly procured volumes vary according to the reserve plans submitted by the balancing service providers and the price is constant over the whole year.
                '''
            }
        }

    def _datasets_values_to_lists(self):
        '''Return list of available variableIds in available dict of available datasets.'''
        available_variableIds = []

        # Get dict of data on the available datasets.
        datasets_dict = self._datasets()

        # Make lists to store information about the available datasets.
        datasets_names_list = []
        datasets_variableIds_list = []
        datasets_formats_list = []
        datasets_info_list = []

        # Loop on the datasets dict.
        for name, value in datasets_dict.items():

            # Store datasets names in list.
            datasets_names_list.append(name)

            # Store datasets variableIds in list.
            datasets_variableIds_list.append(value["VariableId"])

            # Store available formats in list.
            datasets_formats_list.append(value["Formats"])

            # Store available info in list.
            datasets_info_list.append(value["Info"])
        
        # Return lists of datasets names and variableIds.
        return datasets_names_list, datasets_variableIds_list, datasets_formats_list, datasets_info_list
    
    
    
    ################################################################
    ############## Frontend functions.
    ################################################################

    def show_parameters(self, include_info=False, return_df=False, tablefmt="grid", savetofilepath=None):
        '''
        Displays available datasets in api as markdown list and possible returns as DataFrame. 
        '''
        # Convert list of format tuples to list of strings before printing.
        formats_str_list = []
        for i in self.static_datasets_formats_list:

            if isinstance(i, tuple):
                formats_str_list.append(', '.join(i))
            else:
                formats_str_list.append(i)

        # Create dict before creating DataFrame.
        df_dict = {
            'Available FingridApi Dataset Names': self.static_datasets_names_list,
            'Dataset VariableIds': self.static_datasets_variableids_list, 
            'Dataset Formats': formats_str_list
        }

        # Add info to dict if spesified.
        if include_info: 
            df_dict["Info"] = self.static_datasets_infos_list
        
        # Create DataFrame.
        df = pd.DataFrame(df_dict)

        # Shift index to count from 1 in table.
        df.index += 1
        
        # Print out DataFrame as Markdown table.
        print(df.to_markdown(tablefmt=tablefmt))

        # Save if spesified filepath.
        if savetofilepath is not None:
            df.to_markdown(buf=savetofilepath, tablefmt=tablefmt)

        # Return DataFrame if spesified.
        if return_df: return df
        else: return None

    def get_data(self, datasets, start_time=None, end_time=None, formatstr="json", n_closematched_datasets=1, closematched_cutoff=0.5, savefolderpath=""):
        '''
        Requesting data from Fingrid Api Service.

        :How to use:
            - Spesify one or multiple requesting dataset names or variableids to make request.
            - To ensure easy use and correct requests, spesified datasets is searched and close matched to lists of the available datasets.
            - If start_time and/or end_time is spesified, returns one DataFrame for the timeperiod for each requesting dataset. 
            - If start_time and end_time is not spesified, returns one DataFrame with most recent available values for all requesting datasets.
            - If savefolderpath is spesified, saves requested data responses in this folder in format {DataSetName}_{FromDatetime}_{ToDatetime}.csv 

        '''

        # If start time is spesified but end_time is not spesified, set end_time to now.
        if start_time is not None and end_time is None:
            end_time = datetime.datetime.now()
        
        # Get datasets and variableids, matched to spesified requested datasets.
        datasets, variableids = self._get_datasets_variableids_matches(
            datasets=datasets, 
            n_closematched_datasets=n_closematched_datasets, 
            closematched_cutoff=closematched_cutoff
            )

        # If no matches found in datasets.
        if variableids is None: 

            # Print message no match found in available databases.
            print("ERROR:\n\tNo matches found in in available databases.\n")
            print("The available databases on Fingrid Api Service is:")
            self.show_available_datasets()

            # Return dict containing errormessage.
            return {'ErrorMessage': 'No matches found in databases'}
        
        # If start_time and end_time is not spesified.
        if start_time is None and end_time is None:

            # Get last events for all requesting datasets.
            df_dict = self._get_all_requests_last_events(variableids, formatstr=formatstr)

        # If start_time and end_time is spesified.
        else:
            
            # Making timeperiod requests
            df_dict = self._get_all_requests_timeperiod_events(variableids, start_time, end_time, formatstr=formatstr)

            # If response is empty, return empty dict with key "No data in requests responses."
            if df_dict is None: 
                return {'ErrorMessage': 'No data in requests responses'}
            
        # If data in response, return requested datasets Name and Responses as Dict of DataFrames
        return df_dict

    def set_apikey(self, api_key):
        self.api_key = api_key
    
    ################################################################
    ############## Backend functions.
    ################################################################
    
    def _fixed_datetimestr(self, yyyymmddhhmmss):
        '''
        Ensure request timestamp string in correct format "YYYY-MM-DDThh:mm:ssZ".
        '''
        

        # If input is datetime object.
        if isinstance(yyyymmddhhmmss, datetime.datetime):

            # Return datetimestr in correct format.
            #d = 
            return datetime.datetime.strftime(yyyymmddhhmmss, self.static_datetimeformat_str)

        # If input is string.
        if isinstance(yyyymmddhhmmss, str):

            # Determine format from string length.
            if len(yyyymmddhhmmss) > 12:
                strformat = "%Y%m%d%H%M%S"
            elif len(yyyymmddhhmmss) > 10:
                strformat = "%Y%m%d%H%M"
            elif len(yyyymmddhhmmss) > 8:
                strformat = "%Y%m%d%H"
            elif len(yyyymmddhhmmss) > 6:
                strformat = "%Y%m%d"
            elif len(yyyymmddhhmmss) > 4:
                strformat = "%Y%m"
            else:
                strformat = "%Y"

            # Create datetime object of datetimestr and input format.
            yyyymmddhhmmss = datetime.datetime.strptime(yyyymmddhhmmss, strformat)

            # Return datetimestr in correct format.
            return datetime.datetime.strftime(yyyymmddhhmmss, self.static_datetimeformat_str)
    
    def _url_timeparameter_substr(self, start_time, end_time):
        '''Constructing part of request url containing start_time and end_time'''

        # Ensure correct timeformat.
        start_time = self._fixed_datetimestr(start_time)
        end_time = self._fixed_datetimestr(end_time)
        
        # Replace ":" with "%3A" in start_time_str and end_time_str.
        start_time_str = start_time.replace(":", "%3A")
        end_time_str = end_time.replace(":", "%3A")

        # Return request url startendtime substring
        return f"start_time={start_time_str}&end_time={end_time_str}"

    def _url_commaseparatedvariableids_substr(self, variableids):
        '''
        Create url substring of multiple variableids used in get_latest request.
        '''
         # Create empty string to contain requests variableids substring.
        url_substr = ""

        # If variableids is list of multiple ids.
        if isinstance(variableids, list):

            # Loop on requesting VariaBleIds.
            for variableid in variableids:

                # If variableid is None, skip.
                if variableid is None: continue
            
                # Add variableid to url string.
                url_substr = url_substr + str(variableid)

                # If not last VariableId in list, add stringpart between VariableIds in url.
                if variableid != variableids[-1] and variableids[-1] is not None:

                    # Add stringpart between VariableIds in url.
                    url_substr = url_substr + "%2C"
        
        # If variableids is not multiple ids.
        else:

            # If variableids is None, return None
            if variableids is None: return None
            
            # Add to single variableid to url str.
            url_substr = url_substr + str(variableids)

        # Return request url variable substring.
        return url_substr   

    def _get_datasets_variableids_matches(self, datasets, n_closematched_datasets=1, closematched_cutoff=0.5):
        '''Returns spesified datasets variableids'''

        # Create emply list for storing matched variableids.
        matched_datasets = []
        matched_variableids = []

        # If datasets is not list of mupltiple datasets.
        if isinstance(datasets, list) == False:

            # Wrap dataset string in list used in later looping.
            datasets = [datasets]

        # Loop on list of spesified datasets.
        for dset in datasets:

            # Skip if spesified dataset is None.
            if dset is None: continue

            # If dset represent int, set as int.
            try:
                int(dset)
                dset = int(dset)
            except ValueError:
                None
                #dset = str(dset)
            # If spesified dataset exist in list of available variable ids.
            if dset in self.static_datasets_variableids_list:

                # Spesified dataset is variableid, append to variableids directly.
                matched_variableids.append(dset)

                # Append matched dataset to list of matched datasets.
                matched_list_idx = self.static_datasets_variableids_list.index(dset)
                matched_dataset = self.static_datasets_names_list[matched_list_idx]
                matched_datasets.append(matched_dataset)
            
            # If spesified dataset was not found direclty in list of available variableids.
            elif isinstance(dset, str):

                # Search list of available dataset names for match on spesified dataset.
                avail_data_list_lowered = [each_string.lower() for each_string in self.static_datasets_names_list]
                matches = difflib.get_close_matches(dset.lower(), avail_data_list_lowered, n=n_closematched_datasets, cutoff=closematched_cutoff)

                # If matches on spesified dataset was found in list of available datasets.
                if len(matches) > 0:
                    
                    # Loop on matches.
                    for match in matches:

                        # Append matched dataset and variableid to lists.
                        matched_list_idx = avail_data_list_lowered.index(match)
                        matched_variableid = self.static_datasets_variableids_list[matched_list_idx]
                        matched_dataset = self.static_datasets_names_list[matched_list_idx]
                        matched_variableids.append(matched_variableid)
                        matched_datasets.append(matched_dataset)
                
                # If not found match on full string in list of strings of available datasets.
                elif isinstance(dset, str):

                    # Find all available datasets containing all inputted keywords.
                    keywords_list = dset.lower().split(" ")

                    # Create initially full list of available dataset names for keyword matching.
                    keyword_matched_list = avail_data_list_lowered

                    # Loop on keywords.
                    for keyword in keywords_list:

                        # Removing dataset names string not containing keyword
                        keyword_matched_list = [i for i in keyword_matched_list if keyword in i]
                    
                    # If list of available dataset names is not empty after keyword matching.
                    if len(keyword_matched_list) > 0:

                        # Loop on remaining datasets. as matched datasets.
                        for name_match in keyword_matched_list:

                            # Append as matched dataset.
                            matched_list_idx = avail_data_list_lowered.index(name_match)
                            matched_variableid = self.static_datasets_variableids_list[matched_list_idx]
                            matched_dataset = self.static_datasets_names_list[matched_list_idx]
                            matched_variableids.append(matched_variableid)
                            matched_datasets.append(matched_dataset)



        
        # If only one variableid in list of variable ids.
        if len(matched_variableids) == 1:

            # Unpack matched lists to single objects.
            matched_variableids = matched_variableids[0]
            matched_datasets = matched_datasets[0]
        
        # If found no matches, set matched to None.
        elif len(matched_variableids) == 0:
            matched_variableids = None
            matched_datasets = None

        # Return the matched datasets and variableids
        return matched_datasets, matched_variableids

    # Limit calls to 10000calls / 24h, per api restrictions.
    @limits(calls=10000, period=60*60*24) 
    def _call_api(self, url):
        '''
        Makes request call to Fingrid Api, returns response.
        '''
        #print(url)
        headers = {'x-api-key': self.api_key }
        response = requests.get(url, headers=headers)
        return response

    def _get_single_request_timeperiod_events(self, variableid, start_time, end_time, formatstr):
        '''
        Requests all data in timeperiod for single dataset.
        '''

        # Create DataFrame for storing all requested data.
        df = pd.DataFrame()

        # Construct timeperiod baseurl.
        baseurl = f"{self.static_baseurl}/variable/{variableid}/events/{formatstr}?" 

        # Store start_time and end_time as list of tuples
        start_datetime = datetime.datetime.strptime(self._fixed_datetimestr(start_time), self.static_datetimeformat_str)
        end_datetime = datetime.datetime.strptime(self._fixed_datetimestr(end_time), self.static_datetimeformat_str)

        timeperiods = [(start_datetime, end_datetime)]
        
        # Create boolean flag for possible multiple request to obtain data for full timeperiod in large requests.
        request_more_data_bool = True
        
        # Begin while loop, looping until finished or worst case 1000 loops.
        c = 0
        while request_more_data_bool:

            # Loop on list of requesting timeperiods.
            for timeperiod in timeperiods:

        
                # Adding timeperiod substr to create full request url.
                timevariables_str = self._url_timeparameter_substr(timeperiod[0], timeperiod[1])
                url = f'{baseurl}{timevariables_str}'

                # Perform timeperiod request.
                response = self._call_api(url)

                # If response dont contain requested data.
                if response.ok == False:

                    # If message that requested row count is too large.
                    if "Requested row count is too large" in response.text:

                        # Split all timeperiods in list of timeperiods at periods centerdatetime.
                        # Loop on list of requesting timeperiods.
                        new_timeperiods = []
                        for timeperiod in timeperiods:



                            # Split timeperiod at centerdatetime, adding the two subtimeperiods to the new timeperiodslist.
                            centertime = timeperiod[0] + (timeperiod[1] - timeperiod[0]) / 2
                            new_timeperiods.append((timeperiod[0], centertime))
                            new_timeperiods.append((centertime, timeperiod[1]))
                        
                        # Setting new list of timeperiods as timeperiods.
                        timeperiods = new_timeperiods
                        
                        # Increment loop counter
                        c += 1

                        # Stop this for loop, starts new loop with new list of timeperiods.
                        break
                
                # If response contains requested data.
                else:

                    # Append DataFrame from response dict json to total request response DataFrame.
                    df = df.append(pd.DataFrame(response.json()))

            # If current timeperiod is last in list of timeperiods.
            #if timeperiod == timeperiods[-1]:

                # Timeperiods request is finished, convert datetime strings to datetime objects.
                #df["start_time"] = pd.to_datetime(df["start_time"])
                #df["end_time"] = pd.to_datetime(df["end_time"])
                
                # return total requests DataFrame
                return df



            # Increment loop counter
            c += 1
                    
    def _get_all_requests_timeperiod_events(self, variableids, start_time, end_time, formatstr="json"):
        '''
        Returns dict of DataFrames containting requesting datasets events in the spesified timeperiod.
        '''
        # If requesting variableids is not list.
        if isinstance(variableids, list) == False:

            # Wrap in list used for looping.
            variableids = [variableids]
        
        # Create dict for storing requested DataFrames.
        df_dict = {}
        
        # Loop on list of variableids.
        for variableid in variableids:

            
            # Getting timeperiod data for spesified dataset variableid.
            df = self._get_single_request_timeperiod_events(variableid, start_time, end_time, formatstr)
            
            # Adding requested dataset Name and DataFrame response to total request dict.
            df_dict[self.static_datasets_names_list[self.static_datasets_variableids_list.index(variableid)]] = df
            
        # Return total request dict of DataFrames.
        return df_dict

    def _get_all_requests_last_events(self, variableids, formatstr='json'):
        '''
        Returns dict of single DataFrame containting all requesting datasets last registered events.
        '''

        # Create DataFrame for storing all requested data.
        df = pd.DataFrame()

        # Construct last event request url.
        url = f"{self.static_baseurl}/variable/event/{formatstr}/{self._url_commaseparatedvariableids_substr(variableids)}"

        # Perform last events request.
        response = self._call_api(url)

        # If response is bad, return dict with DataFrame cintaining errormessage.
        if response.ok == False:
            errordict = {}
            errordict["ErrorMessage"] = pd.DataFrame([response.json()])
            return response.json()
        
        # If response is OK.
        else:

            # Create DataFrame from response dict.
            df = pd.DataFrame(response.json())

            # Add column of dataset names
            ds_names = []
            
            for idx, row in df.iterrows():
                ds_names.append(self.static_datasets_names_list[self.static_datasets_variableids_list.index(row["variable_id"])])
            df["dataset_name"] = ds_names

            # Rearrange order of columns.
            df = df[['dataset_name', 'variable_id', 'start_time', 'end_time', 'value']]

            # Convert datetime strings to datetime objects.
            df['start_time'] = pd.to_datetime(df['start_time'])
            df['end_time'] = pd.to_datetime(df['end_time'])
            
            # Create response dict containing DataFrame.
            df_dict = {}
            df_dict["Datasets Last Events"] = df

            # Return dict containing DataFrame of datasets last events.
            return df_dict 


################################################################
############## Test functions.
################################################################

def test_get_example(fingrid_api_key, datasets = ["Hydro", "Nuclear"], start_time = '20210101', end_time = None):
    '''Runs example test of use of the api client service.'''
    
    # Create fingridapi client object.
    fingrid_client = FingridOpenDataClient(fingrid_api_key=fingrid_api_key)

    # Show available fingridapi datasets.
    fingrid_client.show_available_datasets()

    # Make request for for Hydro and Nuclear power productions from start time til today.
    responsedata_dict = fingrid_client.get_data(datasets = datasets, start_time = start_time, end_time = end_time)

    # Print out preview of the data respons heads.
    for datasetname, data_df in responsedata_dict.items():
        print(f"Response dataset name: {datasetname}")
        print("Data response:")
        print(data_df.head())

def test_get_all_datasets_timeperiod_events(fingrid_api_key, printout_response=True, start_time = '20210101', end_time = None):
    '''
    Test function, requesting data on timeperiod events for all available fingridapi datasets.
    - If start_time is spesified, get_data will perform request for timeperiod events.
    - If end_time is None, end_time is automatically set to the present time of the request.
    - Returns dict containing individual DataFrames for each requesting dataset data response.
    '''

    # Create fingridapi client object.
    fingrid_client = FingridOpenDataClient(fingrid_api_key=fingrid_api_key)

    # Show available fingridapi datasets.
    fingrid_client.show_available_datasets()

    # Store list of all available datasets.
    all_available_datasets_names = fingrid_client.static_datasets_names_list

    # Make request for for Hydro and Nuclear power productions from start time til today.
    responsedata_dict = fingrid_client.get_data(datasets = all_available_datasets_names, start_time = start_time, end_time = end_time)

    # Print out preview of the data respons heads.
    if printout_response:
        for responsename, responsedata_df in responsedata_dict.items():
            print(f"Response dataset name: {responsename}")
            print("Data response:")
            print(responsedata_df.head())
    
    # Return request response data.
    return responsedata_dict

def test_get_all_datasets_last_events(fingrid_api_key, printout_response=True):
    '''
    Test function, requesting data on last events for all available fingridapi datasets.
    - If start_time and end_time is not spesified, get_data() will perform request for last events.
    - Returns dict containing single DataFrame where each requesting dataset data response is included as rows.
    '''

    # Create fingridapi client object.
    fingrid_client = FingridOpenDataClient(fingrid_api_key=fingrid_api_key)

    # Show available fingridapi datasets.
    fingrid_client.show_available_datasets()

    # Store list of all available datasets.
    all_available_datasets_variableids = fingrid_client.static_datasets_variableids_list

    # Make request for for Hydro and Nuclear power productions from start time til today.
    responsedata_dict = fingrid_client.get_data(datasets = all_available_datasets_variableids)

    # Print out preview of the data respons heads.
    if printout_response:
        for responsename, responsedata_df in responsedata_dict.items():
            print(f"Response dataset name: {responsename}")
            print("Data response:")
            print(responsedata_df)

    # Return request response data.
    return responsedata_dict

# Main
if __name__ == "__main__":
    print("You ran fingridapi.py directly.")
    
    #fingrid_api_key = "22"
    #fingrid_api_key = "your fingrid api key"
    
    # Run example test of use of fingridapi client.
    #test_get_example(fingrid_api_key = fingrid_api_key)

    #fingrid_client = FingridClient(fingrid_api_key=fingrid_api_key)

    #response_dict = test_get_all_datasets_last_events(fingrid_api_key=fingrid_api_key)

   