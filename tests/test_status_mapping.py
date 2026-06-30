from src.utils.config import STATUS_MAPPING


def test_status_mapping_contains_active():
    assert STATUS_MAPPING["ACTIVE"] == "Active"
