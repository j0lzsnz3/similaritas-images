class Employee:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def toJSON(self):
        return {"Employees": {'firstName': self.first_name,
                              'lastName': self.last_name}}