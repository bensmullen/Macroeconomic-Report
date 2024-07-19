import os
import pandas as pd
import requests
from datetime import datetime

class FRED:
    earliest_realtime_start = '1776-07-04'
    latest_realtime_end = '9999-12-31'
    today = datetime.today().strftime('%Y-%m-%d')
    nan_char = '.'
    max_results_per_request = 1000
    base_url = 'https://api.stlouisfed.org/'

    # Initialize FRED object
    def __init__(self, api_key=None, api_key_file=None):

        """
        Initialize the FRED class that has functions for grabbing economic data from the FRED website. Can be obtained from the FRED website at https://fred.stlouisfed.org/docs/api/api_key.html

        Parameters:
        api_key : str
            FRED API key
        
        api_key_file : str
            Path to the file containing the FRED API key
        """

        self.api_key = None
        if api_key is not None:
            self.api
        elif api_key_file is not None:
            file = open(api_key_file, 'r')
            self.api_key = file.readline().strip()
            file.close()
        else:
            self.api_key = os.environ.get('FRED_API_KEY')

        if self.api_key is None:
            import textwrap
            raise ValueError(textwrap.dedent("""\
                                             No valid FRED API key was found. You can set the API key by doing one of the following:
                                             pass the API key string using parameter "api_key", pass the path to the API key using the
                                             parameter "api_key_file", or setting an environement variable 'FRED_API_KEY' to the value
                                             of your API key.
                                             """))
        

    # Put API response into Pandas DataFrame
    def get_data(response):
        if response.status_code == 200:
            res_data = response.json()
            release_df = pd.DataFrame(res_data)
            return release_df
        else:
            print('Failed to retrieve data. Status Code: ', response.status_code)

    # Get time series economic data
    def get_series(self, series_id, realtime_start=today, realtime_end=today, limit=100000, offset=0, sort_order='asc', observation_start=earliest_realtime_start, observation_end=latest_realtime_end, units='lin', frequency=None, aggregation_method='avg', output_type=1, vintage_dates=None):

        param_dict = {
            'api_key' : self.api_key,
            'file_type' : 'json',
            'series_id' : series_id,
            'realtime_start' : realtime_start,
            'realtime_end' : realtime_end,
            'limit' : limit,
            'offset' : offset,
            'sort_order' : sort_order,
            'observation_start' : observation_start,
            'observation_end' : observation_end,
            'units' : units,
            'frequency' : frequency,
            'aggregation_method' : aggregation_method,
            'output_type' : output_type,
            'vintage_dates' : vintage_dates
        }

        response = requests.get(base_url+'fred/series/observations', params=param_dict)

        series_df = get_data(response)

        return series_df

