import numpy as np
import pandas as pd
from pytest import approx

def compute_analysis(dataframe) -> dict:

    return {"min": np.min(dataframe["base_experience"]),
            "max": np.max(dataframe["base_experience"]),
            "mean": np.mean(dataframe["base_experience"]),
            "median": np.median(dataframe["base_experience"]),
            }

def test_compute_analysis():
    inputs = pd.DataFrame.from_dict({
        'base_experience': [10,15,20],
        'height': [10,15,20],
        'id': [1,2,3],
        'species': ['x','y','z'],
        'type1': ['type1.0','type1.1','type1.2'],
        'type2': ['type2.0','type2.1','type2.2'],
        'weight': [60,70,80]})
    exp_output = {
        "min":10,
        "max":20,
        "mean":15,
        "median":15
    }
    actual_output = compute_analysis(inputs)
    assert actual_output["min"]== approx(exp_output["min"], rel=1e-3, abs=1e-3)
    assert actual_output["max"]== approx(exp_output["max"], rel=1e-3, abs=1e-3)
    assert actual_output["mean"]== approx(exp_output["mean"], rel=1e-3, abs=1e-3)
    assert actual_output["median"]== approx(exp_output["median"], rel=1e-3, abs=1e-3)
