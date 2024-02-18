from typing import Any
import yaml
import requests
import pandas as pd
import logging

class Analysis():

    def __init__(self, analysis_config: str) -> None:
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
        The configuration files include parameters for:
            * Pokemon API token
            * ntfy.sh topic
            * Default save path

        '''
        logging.basicConfig(level=logging.INFO)
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']
    
        if not analysis_config.endswith('.yml'):
            logging.error('analysis_config path must be a path to a yml file')
            raise ValueError('analysis_config path must be a path to a yml file')

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            try:
                with open(path, 'r') as f:
                    this_config = yaml.safe_load(f)
                config.update(this_config)
            except TypeError as e:
                e.add_note(f"Config file '{path}' is empty")
                raise e

        assert(config['ntfy_topic_name'])
        assert(config['job_dir_path'])
        assert(config['poke_id_start_of_range'] is not None)
        assert(config['poke_id_end_of_range'])
        assert(isinstance(config['poke_id_start_of_range'], int))
        assert(isinstance(config['poke_id_end_of_range'], int))
        assert(config['poke_id_start_of_range'] > 0)

        self.config = config

        logging.info(f'CONFIG LOADED: {self.config}')
    
    def get_poke_dict(self, id) -> dict | None:
        '''
         A helper function to obtain files from API, and parse for 'base_experience', 'height', 'id', 'species', 'types', and 'weight' to get a dictionary.
        
        Parameters
        ----------
        id : dict

        Returns
        -------
        Dictionary | None
        '''
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

    def get_poke_df(self, list_of_ids) -> pd.DataFrame:
        '''
        A helper function to obtain a DataFrame from the retrieved data.

        Parameters
        ----------
        list_of_ids : list

        Returns
        -------
        poke_df : DataFrame
            DataFrame of 'base_experience', 'height', 'id', 'species', 'types', and 'weight' 
        '''
        poke_dicts = []
        poke_df = pd.DataFrame()
        for id in list_of_ids:
            new_poke_dict = self.get_poke_dict(id)
            if new_poke_dict is not None:
                poke_dicts.append(new_poke_dict)
            poke_df = pd.DataFrame(poke_dicts)
        return poke_df

    def load_data(self) -> None:
        ''' Retrieve data from the Pokemon API

            This function makes an HTTPS request to the Pokemon API and retrieves your selected data. The data is
            stored in the Analysis object.

            Parameters
            ----------
            None

            Returns
            -------
            None

            '''
        
        #load the start and end pokemon ID numbers from the config
        #add 1 to the end variable (poke_id_end_of_range) before creating the range so the last pokemon doesn't get delete
        list_of_ids = range(self.config['poke_id_start_of_range'], self.config['poke_id_end_of_range'] + 1) #load data
        poke_df = self.get_poke_df(list_of_ids)
        logging.info(f'loaded data: \n{poke_df}')

        self.dataset = poke_df

    def compute_analysis(self) -> Any:
        ''' Analyze previously-loaded data.

            This function runs an analytical measure of mean, median, min, max.
            and returns the data in a dictionary.

            Parameters
            ----------
            dataset

            Returns
            -------
            analysis_output : Dictionary

            '''
        condensed_dataset = self.dataset[["base_experience", "height", "weight"]]

        condensed_dict = {"mean": condensed_dataset.mean(),
                          "median": condensed_dataset.median(),
                          "min": condensed_dataset.min(),
                          "max": condensed_dataset.max()
                          }
        
        self.notify_done("Analysis Complete!")

        return condensed_dict

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
    
        topic = self.config['ntfy_topic_name']

        requests.post(f"https://ntfy.sh/{topic}", data=message.encode(encoding='utf-8'))
        
