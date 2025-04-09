import json
from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [ { 'id': 1, 'name': 'Ashley' }, { 'id': 2, 'name': 'Kate' }, { 'id': 3, 'name': 'Joe' }]

@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees) , 200

@app.route('/employees/<int:idx>', methods=['GET'])
def get_employee(idx:int,internal=True):
    global employees
    if len([e for e in employees if e["id"] == idx]) == 0 :
        return jsonify({'error': 'Employee does not exist.'}), 404
    else:
        return jsonify([e for e in employees if e["id"] == idx]) , 200

@app.route('/employees/<int:idx>', methods=['DELETE'])
def del_employees(idx : int):
    global employees
    if not check_employee_by_id(idx):
        return jsonify({'error': 'Employee does not exist.'}), 404
    employees = [e for e in employees if e['id'] != idx]
    return jsonify(employees) , 200

@app.route('/employees', methods=['POST'])
def create_employee():
    new_employee = json.loads(request.data)
    for key in new_employee.keys():
        if key == "name":
            new_id = get_max_id() + 1
            new_employee['id'] = new_id
            employees.append(new_employee)
            return '', 201, {'location': f'/employees/{new_id}'}
        else:
            return jsonify({"Error":"Arguments invalides"}), 500

@app.route('/employees/<int:idx>', methods=['PUT'])
def update_employee(idx : int):
    global employees
    if len([e for e in employees if e["id"] == idx]) == 0:
        return jsonify({'error': 'Employee does not exist.'}), 404
    else:
        new_employee_data = json.loads(request.data)
        for key in new_employee_data.keys():
            if key == "name":
                employee = get_employee_by_id(idx)[0]
                employee.update(new_employee_data)
                return jsonify({'success': employee}), 200

def get_max_id():
    global employees
    max_id = max(e['id'] for e in employees)
    return max_id

def check_employee_by_id(idx: int):
    global employees
    if len([e for e in employees if e["id"] == idx]) == 0:
        return False
    else:
        return True

def get_employee_by_id(idx: int):
    global employees
    return [e for e in employees if e["id"] == idx]


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0',port=5000)