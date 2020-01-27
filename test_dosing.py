import pytest
from dosing import Dosing

@pytest.fixture
def dosing():
    return Dosing("t2_ec 20190619.csv", "t2_registry 20190619.csv", "results.csv")

@pytest.mark.parametrize('''viscode, svdose, ecsdstxt, 
                            expected_ec_row_count, expected_registry_row_count, expected_merged_row_count, expected_merged_filtered_row_count,
                            expected_result_col_count, expected_ids, expected_rids, expected_userids, expected_ecsdstxts''', [
    ('w02', 'Y', 280, 11, 14, 14, 2, 6, [30, 32], [19, 17], ['MORPHEUS_UCSD_EDU_2', 'MORPHEUS_UCSD_EDU'], [-4, 140]),
    ('w10', 'Y', 280, 11, 14, 14, 0, 6, None, None, None, None)
])
def test_merge_filtered(dosing, viscode, svdose, ecsdstxt, 
                        expected_ec_row_count, expected_registry_row_count, expected_merged_row_count, expected_merged_filtered_row_count,
                        expected_result_col_count, expected_ids, expected_rids, expected_userids, expected_ecsdstxts):
    #test init
    ec_actual_row_count = dosing.data_ec.shape[0]
    assert ec_actual_row_count == expected_ec_row_count, "ec dataframe contains {0} rows, expecting {1}".format(ec_actual_row_count, expected_ec_row_count)

    registry_actual_row_count = dosing.data_registry.shape[0]
    assert registry_actual_row_count == expected_registry_row_count, "registry dataframe contains {0} rows, expecting {1}".format(registry_actual_row_count, expected_registry_row_count)

    #test merge
    merged_data = dosing._Dosing__merge()
    merged_actual_row_count = merged_data.shape[0]
    print(merged_actual_row_count)
    assert merged_actual_row_count == expected_merged_row_count, "merged dataframe contains {0} rows, expecting {1}".format(merged_actual_row_count, expected_merged_row_count)

    #test merged & filtered
    #row count
    merge_filtered_data = dosing._Dosing__report_filter(merged_data, viscode, svdose, ecsdstxt)
    actual_merged_filtered_row_count = merge_filtered_data.shape[0]
    assert actual_merged_filtered_row_count == expected_merged_filtered_row_count, "merged & filtered dataframe contains {0} rows, expecting {1}".format(merged_filtered_actual_row_count, expected_merged_filtered_row_count)
    #col count
    actual_result_col_count = len(merge_filtered_data.columns)
    assert actual_result_col_count == expected_result_col_count
    #filters and expected results
    if (expected_merged_filtered_row_count > 0):
        for i in range(actual_merged_filtered_row_count):
            assert merge_filtered_data['VISCODE'].values[i] == viscode
            assert merge_filtered_data['SVDOSE'].values[i] == svdose
            assert merge_filtered_data['ECSDSTXT'].values[i] != ecsdstxt
            assert merge_filtered_data['ID'].values[i] in expected_ids
            assert merge_filtered_data['RID'].values[i] in expected_rids
            assert merge_filtered_data['USERID'].values[i] in expected_userids
            assert merge_filtered_data['ECSDSTXT'].values[i] in expected_ecsdstxts
            

