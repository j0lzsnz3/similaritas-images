from flask import Flask, json
from employee import Employee
import names

app = Flask(__name__)


@app.route('/employee')
def get_employee():
    global json_str
    try:
        employee_list = []

        for i in range(0, 5):
            employee = Employee(names.get_first_name(), names.get_last_name())
            employee_list.append(employee)

        json_str = json.dumps([e.toJSON() for e in employee_list])

    except:
        print("Error")

    return json_str


if __name__ == '__main__':
    app.run()
