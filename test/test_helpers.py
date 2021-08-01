import pytest

from helpers import Equipment, Inventory


def test_inventory_init_from_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    p.write_text('{"test": {"name": "test"}}')
    inventory = Inventory(p)
    assert inventory.test.to_dict() == {'name': 'test'}


def test_inventory_init_from_empty_file(tmp_path):
    inventory = Inventory('sub/test.json')
    assert inventory.__dict__ == {'_db_file': 'sub/test.json'}


def test_inventory_dumps_to_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    inventory = Inventory(p)
    inventory.test = Equipment({'name': 'test'})
    inventory.sync()
    assert p.read_text() == '{"test": {"name": "test"}}'


def test_inventory_add_equipment(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    inventory = Inventory(p)
    inventory.add_equipment({'name': 'test'})
    assert inventory.test.to_dict() == {'name': 'test'}


def test_inventory_get_equipment(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    inventory = Inventory(p)
    inventory.add_equipment({'name': 'test1'})
    inventory.add_equipment({'name': 'test2'})
    assert inventory.get_equipment() == ['test1', 'test2']


def test_inventory_get_equipment_attr(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    inventory = Inventory(p)
    inventory.add_equipment({'name': 'test', 'get_me': 'got_me'})
    assert inventory.get_equipment_attr('test', 'get_me') == 'got_me'


def test_inventtory_update_equipment_attr(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    inventory = Inventory(p)
    inventory.add_equipment({'name': 'test', 'change_me': 'before'})
    inventory.update_equipment_attr('test', {'change_me': 'after'})
    assert inventory.test.change_me == 'after'


def test_inventory_del_equipment(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    inventory = Inventory(p)
    inventory.add_equipment({'name': 'test1'})
    inventory.add_equipment({'name': 'test2'})
    inventory.del_equipment('test1')
    assert inventory.get_equipment() == ['test2']
