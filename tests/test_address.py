from src.transformations.address import split_address


def test_split_address_empty():
    assert split_address("") == ("", "", "")


def test_split_address_limits():
    street_1, street_2, street_3 = split_address("10 avenue des exemples anonymes batiment nord", [10, 20, 20])
    assert len(street_1) <= 10
    assert len(street_2) <= 20
    assert len(street_3) <= 20
