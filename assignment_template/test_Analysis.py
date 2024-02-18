import pytest

def test_load_data():
    import Analysis
    
    analysis_obj = Analysis.Analysis("configs/job_file.yml")
    analysis_obj.load_data()
    analysis_output = analysis_obj.compute_analysis()

    assert analysis_obj.dataset.shape == (3, 7)
    assert analysis_output['mean']['height'] == pytest.approx(12.3333, 0.0001)
    assert analysis_output['median']['weight'] == 130
    assert analysis_output['min']['base_experience'] == 64
    assert analysis_output['max']['base_experience'] == 263

    print(analysis_output)
