import pandas, pytest
from dosing import Dosing

@pytest.fixture
def dosing():
    return Dosing("t2_ec 20190619.csv", "t2_registry 20190619.csv", "results.csv")

def test_create_report(dosing):
    #case: 'w02', 'Y', 280
    test_df = pandas.DataFrame({"ID": [30, 32], "RID": [19, 17], "USERID": ["MORPHEUS_UCSD_EDU_2", "MORPHEUS_UCSD_EDU"], 
                                "VISCODE": ["w02","w02"], "SVDOSE": ["Y", "Y"], "ECSDSTXT": [-4.0, 140.0]})
    dosing.create_report('w02', 'Y', 280)
    pandas.testing.assert_frame_equal(dosing.merged_filtered_df.reset_index(drop=True), test_df.reset_index(drop=True))

    #case: empty
    dosing.create_report('w10', 'Y', 280)
    assert dosing.merged_filtered_df.empty
