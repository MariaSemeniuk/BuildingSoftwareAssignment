from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import pandas as pd
import logging

"""
in __init__,  pass into the config the start and end of a range of pokemon numbers that we want to analyze
- it will save the config as self.config and not return anything

we will use the get_poke_df as our load_data
- instead of passing in the list, we will load the start and end numbers from the config
- we will also use the get_poke_data function as a helper function, which just means that it doesn't get directly called by the end user
- it will store the data to self.dataset

in compute_analysis, we will calculate the mean, min, or max of self.dataset
- we will need to put the calculation function in the config
- it will call notify_done with a message that includes if we calculated min, mean, or max

in notify_done, we will write to ntfy.sh
""" 

"""

in get_data

make sure you can load self.config
make sure you can load the start and end variables out of self.config
make sure you can create a range using the start and end variables
make sure you add 1 to the end variable before creating the range so the last pokemon doesnt get delete
call get_poke_data like in get_poke_df
save the df to self.dataset
"""
"""
for unit testing

test get_poke_data with a single id and make sure it returns the data you want
test get_poke_df with a list of ids and make sure the dataframe has the correct shape
test compute_analysis by calling get_poke_df with a list of ids and returning the mean of the output dataframe, and make sure that it matches what you'd expect
"""
def get_poke_dict(id):
    url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        r_json = response.json()
        poke_dict = {}
        keys = ['base_experience', 'height', 'id', 'species', 'types', 'weight']
        for key in keys:
            if key == 'species':
                poke_dict[key] = r_json[key]['name']
                
            elif key == 'types':
                for poke_type in r_json[key]:
                    if poke_type ['slot'] == 1:
                        poke_dict['type1'] = poke_type['type']['name']
                    else:
                        poke_dict['type2'] = poke_type['type']['name']                
            else:
                poke_dict[key] = r_json[key]

        return poke_dict
    else:
        return None

def get_poke_df(list_of_ids):
    poke_dicts = []
    for id in list_of_ids:
        new_poke_dict = get_poke_dict(id)
        if new_poke_dict is not None:
            poke_dicts.append(new_poke_dict)
        poke_df = pd.DataFrame(poke_dicts)
    return poke_df



class Analysis():


    def __init__(self, analysis_config: str) -> None:

        logging.basicConfig(level=logging.INFO)
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']
        ''' Load config into an Analysis object

        Load system-wide configuration from `configs/system_config.yml`, user configuration from
        `configs/user_config.yml`, and the specified analysis configuration file

        Parameters
        ----------
        analysis_config : str
            Path to the analysis/job-specific configuration file

        Returns
        -------
        analysis_obj : Analysis
            Analysis object containing consolidated parameters from the configuration files

        Notes
        -----
        The configuration files should include parameters for:
            * GitHub API token
            * ntfy.sh topic
            * Plot color
            * Plot title
            * Plot x and y axis titles
            * Figure size
            * Default save path

        '''

        if not analysis_config.endswith('.yml'):
            logging.error('analysis_config path must be a path to a yml file')
            raise ValueError('analysis_config path must be a path to a yml file')

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)

        assert(config['ntfy_topic_name'])
        assert(config['job_dir_path'])
        assert(config['poke_id_start_of_range'] is not None)
        assert(config['poke_id_end_of_range'])
        assert(isinstance(config['poke_id_start_of_range'], int))
        assert(isinstance(config['poke_id_end_of_range'], int))

        self.config = config

        logging.info(f'CONFIG LOADED: {self.config}')

    def load_data(self) -> None:
        ''' Retrieve data from the GitHub API

            This function makes an HTTPS request to the GitHub API and retrieves your selected data. The data is
            stored in the Analysis object.

            Parameters
            ----------
            None

            Returns
            -------
            None

            '''
        data = requests.get('/url/to/data').json()
        self.dataset = data
        print(self.config['figure_title'])

    def compute_analysis(self) -> Any:
        ''' Analyze previously-loaded data.

            This function runs an analytical measure of your choice (mean, median, linear regression, etc...)
            and returns the data in a format of your choice.

            Parameters
            ----------
            None

            Returns
            -------
            analysis_output : Any

            '''
        return self.dataset.mean() 


    def notify_done(self, message: str) -> None:
        ''' Notify the user that analysis is complete.

            Send a notification to the user through the ntfy.sh webpush service.

            Parameters
            ----------
            message : str
            Text of the notification to send

            Returns
            -------
            None

            '''
        pass

#Just for testing: 
job1 = Analysis('/Users/mariasemeniuk/Documents/DSI-noGithubStuff/BuildingSoftwareAssignment/job1/configs/job_file.yml')
#job1.load_data() #TODO