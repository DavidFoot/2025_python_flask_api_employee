import json
from flask import Flask, jsonify, request
from sqlalchemy import *

app = Flask(__name__)
# SQLAlchemy

engine = create_engine("sqlite:///employee.db", echo=True)
metadata_obj = MetaData()
employee_table  = Table(
    "employee",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("age", Integer)
    )
metadata_obj.create_all(engine)

@app.route('/employees', methods=['GET'])
def get_employees():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM employee"))
        employees_output = [dict(row._mapping) for row in result]
        return jsonify(employees_output), 200
@app.route('/test_table_employee', methods=['GET'])
def test_create_employee():
    with engine.connect() as conn:
        try:
            result = conn.execute(text("SELECT * FROM employee LIMIT 1"))
            return jsonify({'message': 'Table employee exists and is accessible.'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
@app.route('/employees/<int:idx>', methods=['GET'])
def get_employee(idx:int):
    if check_employee_by_id(idx):
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM employee WHERE id = {idx}"))
            res = [dict(row._mapping) for row in result]
            return jsonify({'success': res}), 200
    else:
        return jsonify({'error': 'Employee does not exist.'}), 404
@app.route('/employees/<int:idx>', methods=['DELETE'])
def del_employees(idx : int):
    if check_employee_by_id(idx) :
        with engine.connect() as conn:
            result = conn.execute(text(f"DELETE FROM employee WHERE id = {idx}"))
            conn.commit()
            return jsonify({'success': 'Employee deleted.'}), 200
    else:
        return jsonify({'error': 'Employee does not exist.'}), 404
@app.route('/employees', methods=['POST'])
def create_employee():
    new_employee = json.loads(request.data)
    stmt = insert(employee_table).values(name=new_employee["name"], age=new_employee["age"])
    with engine.connect() as sqla_connection:
        result = sqla_connection.execute(stmt)
        sqla_connection.commit()
        return jsonify({'id': result.inserted_primary_key[0], 'name': new_employee["name"], 'age': new_employee["age"]}), 201
@app.route('/employees/<int:idx>', methods=['PUT'])
def update_employee(idx : int):
    if check_employee_by_id(idx):
        update_data_employee = json.loads(request.data)
        with engine.connect() as conn:
            query = employee_table.update().values(name=update_data_employee["name"], age=update_data_employee["age"]).where(employee_table.c.id == f"{idx}")
            conn.execute(query)
            conn.commit()
            return jsonify({'success': 'Employee Updated.'}), 200
    else:
        return jsonify({'error': 'Employee does not exist.'}), 404

#Utils
def check_employee_by_id(idx: int):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM employee where id = {idx}"))
        if len(list(result)) > 0 :
            return True
        return False


# no more Needed
def get_max_id():
    global employees
    max_id = max(e['id'] for e in employees)
    return max_id
def get_employee_by_id(idx: int):
    global employees
    return [e for e in employees if e["id"] == idx]

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0',port=5000)