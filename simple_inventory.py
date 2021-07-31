from flask import Flask, jsonify, request
from helpers import Inventory

app = Flask(__name__)


@app.route('/inventory/', methods=['GET'])
def get_inventory():
    """Returns the list of equipment"""
    return jsonify({'equipment': [inventory.get_equipment()]})


@app.route('/inventory/<name>', methods=['GET'])
def get_equipment_by_name(name):
    """Returns the equipment instance"""
    return jsonify(getattr(inventory, name).to_dict())


@app.route('/inventory/<name>/<attr>', methods=['GET'])
def get_equipment_by_attr(name, attr):
    """Returns the specified attribute of equipment"""
    return jsonify(inventory.get_equipment_attr(name, attr))


@app.route('/inventory/', methods=['POST'])
def add_equipment():
    """Adds new equipment with JSON provided"""
    equipment = inventory.add_equipment(request.json)
    return jsonify({'name': equipment}), 201


@app.route('/inventory/<name>', methods=['DELETE'])
def del_equipment(name):
    """Deletes an equipment by name"""
    equipment = inventory.del_equipment(name)
    return jsonify(equipment), 200


@app.route('/inventory/<name>', methods=['PUT'])
def update_equipment_attr(name):
    """Updates an attribute in equipment with JSON provided"""
    updated_equipment = inventory.update_equipment_attr(name, request.json)
    return jsonify(updated_equipment), 200


if __name__ == '__main__':
    inventory = Inventory('db.json')
    app.run(host='0.0.0.0')
