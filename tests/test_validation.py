from src.transformations.address import split_address


def test_address_split_keeps_three_fields():
    result = split_address("12 avenue de la migration enterprise data platform", [10, 15, 20])
    assert len(result) == 3


def test_address_split_empty_value():
    assert split_address("", [60, 40, 40]) == ("", "", "")
