from request_data import request
import os
print(os.getcwd())
re = request("student_data.json")
database = re.request_access()
re.update_access(database)