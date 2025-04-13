from ipc.get_ipc import calculate_compound_interest


def test_calculate_compound_int_andorra():

    compounded_ipc = calculate_compound_interest(2023, 2024)
    assert round(compounded_ipc, 2) == 7.32
