from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests
import numpy as np
import pandas as pd


class Analysis():

    def __init__(self, analysis_config: str) -> None:
        CONFIG_PATHS = ['configs/system_config.yml', 'configs/user_config.yml']

        # add the analysis config to the list of paths to load
        paths = CONFIG_PATHS + [analysis_config]

        # initialize empty dictionary to hold the configuration
        config = {}

        # load each config file and update the config dictionary
        for path in paths:
            with open(path, 'r') as f:
                this_config = yaml.safe_load(f)
            config.update(this_config)

        self.config = config

    def load_data(self) -> None:
        print(self.config['figure_title'])

    def compute_analysis(self) -> dict:
        '''Analyze previously-loaded data.

        This function compute several statistics of pokemons' base_experience 

        Parameters
        ----------
        None

        Returns
        -------
        analysis_output : Dictionary that contains min, max, mean, median of
        the pokemons' base_experience

        '''
        
        return {"min": np.min(self.dataset["base_experience"]),
                "max": np.max(self.dataset["base_experience"]),
                "mean": np.mean(self.dataset["base_experience"]),
                "median": np.median(self.dataset["base_experience"]),
                }

    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        pass

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
        topic = 'building-software-assignemt-analysis'
        message = message

        # send a message through ntfy.sh
        requests.post(
            'https://ntfy.sh/' + topic,
            data=message.encode('utf-8'),
        )
    