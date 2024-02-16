from typing import Any, Optional
import matplotlib.pyplot as plt
import yaml
import requests


class Analysis():


    def __init__(self, analysis_config: str) -> None:
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
        print(self.config['figure_title'])

    def compute_analysis(self) -> Any:
        '''Analyze previously-loaded data.

            This function runs an analytical measure of your choice (mean, median, linear regression, etc...)
            and returns the data in a format of your choice.

            Parameters
            ----------
            None

            Returns
            -------
            analysis_output : Any

            '''
        pass


        #Optional
    def plot_data(self, save_path: Optional[str] = None) -> plt.Figure:
        ''' Analyze and plot data

            Generates a plot, display it to screen, and save it to the path in the parameter `save_path`, or 
            the path from the configuration file if not specified.

            Parameters
            ----------
            save_path : str, optional
                Save path for the generated figure

            Returns
            -------
            fig : matplotlib.Figure

            '''
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
        pass
    