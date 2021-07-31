import pytest

from helpers import Inventory


def test_inventory_init_from_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    p.write_text('{"test": {"name": "test"}}')
    inventory = Inventory(p)
    assert inventory.test.to_dict() == {'name':'test'}
