# There are no non-automated tests.
* The following tests are automated. 

# All tests found in Analysis.py except test_analysis unit test file. 

* test_Analysis file tests the load data function from Analysis file for specific parameters if looking at the first 3 pokemon in range and comuputing analysis


# The following is found in the Analysis.py file.

* logging the bacisConfig
logging.basicConfig(level=logging.INFO)


* checking if the config file is .yml
if not analysis_config.endswith('.yml'):
    logging.error('analysis_config path must be a path to a yml file')
    raise ValueError('analysis_config path must be a path to a yml file')



* load each config file and update the config dictionary with try and except, ad raising an error if config file path is empty.

for path in paths:
    try:
        with open(path, 'r') as f:
            this_config = yaml.safe_load(f)
        config.update(this_config)
    except TypeError as e:
        e.add_note(f"Config file '{path}' is empty")
        raise e

* checking the config files
assert(config['ntfy_topic_name'])
assert(config['job_dir_path'])
assert(config['poke_id_start_of_range'] is not None)
assert(config['poke_id_end_of_range'])
assert(isinstance(config['poke_id_start_of_range'], int))
assert(isinstance(config['poke_id_end_of_range'], int))
assert(config['poke_id_start_of_range'] > 0)


* logging the loaded config
logging.info(f'CONFIG LOADED: {self.config}')

* logging the loaded dataframe
logging.info(f'loaded data: \n{poke_df}')
