import os
import json

from flask import Flask, request, abort, g
from flask_cors import CORS, cross_origin

from backend.app_api import AppAPI

app = Flask(__name__)
CORS(app, support_credentials=True)

# App configuration
app.config['CORS_HEADERS'] = 'Content-Type'

# Configuration variables
api_path = "/api/v1"
db_path = os.environ.get("DB_PATH")


# Application components
def get_api():
    api = getattr(g, "_api", None)
    if api is None:
        api = g._api = AppAPI(database_path=db_path)
    return api


# Base application routers
@app.route('/')
def home_handler():
    return 'Please use the API at /api/v1/!'


@app.route(f'{api_path}/auth/', methods=['POST'])
def api_auth():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "password" not in body.keys():
        abort(401, description="Information not given!")

    # Attempt to authenticate the user
    raw_result = api.authenticate(username=body["username"], password=body["password"])

    # Verify authentication was successful
    if raw_result is None:
        abort(401, description="Could not authorize!")

    # Unpack raw_result
    auth_token, privileges = raw_result
    del raw_result

    # Build response and return information
    response = f'''{{ \"auth_token\": \"{auth_token.token_content}\", \"expiration\": \"{auth_token.expiration}\", 
    \"privileges\": {json.dumps(privileges)}}} '''
    return json.loads(response)


@app.route(f'{api_path}/auth/logout', methods=['POST'])
def api_logout():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys():
        abort(500, description="Information not given!")

    # Perform logout
    result = api.logout(username=body["username"], token=body["token"])

    # Return the status
    return f"{{ success: {result} }}"


# Student application routers
@app.route(f'{api_path}/student/my_courses', methods=['POST'])
def student_my_courses():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys():
        abort(500, description="Information not given!")

    # Get student's courses
    # [TODO] Change student_name to the actual student's name
    courses = api.see_associated_classes(username=body["username"], token=body["token"])

    # Return the courses as JSON
    return json.dumps(courses)


@app.route(f'{api_path}/student/all_courses', methods=['POST'])
def student_all_courses():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys():
        abort(500, description="Information not given!")

    # Get list of courses + course info
    courses = api.see_courses(username=body["username"], token=body["token"], spots_available=False)

    # Return the courses as JSON
    return json.dumps(courses)


@app.route(f'{api_path}/student/register_course', methods=['POST'])
def student_register_course():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys() and "course_id" not in body.keys():
        abort(500, description="Information not given!")

    # Get list of courses + course info
    result = api.register_for_course(username=body["username"], token=body["token"], course_abbreviation=body["course_id"])

    # Return the whether the registration was successful
    return json.dumps(f"{{ success: {result} }}")


# Instructor application routers
@app.route(f'{api_path}/instructor/course_students', methods=['POST'])
def instructor_get_students():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys() or "course_id" not in body.keys():
        abort(500, description="Information not given!")

    # Get list of students as tuples
    course_students = api.see_course_students(username=body["username"], token=body["token"],
                                              course_abbreviation=body["course_id"])

    # Return the students as JSON
    return json.dumps(course_students)


@app.route(f'{api_path}/instructor/my_courses', methods=['POST'])
def instructor_my_courses():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys():
        abort(500, description="Information not given!")

    # Get instructor's courses
    courses = api.see_teaching_courses(username=body["username"], token=body["token"])

    # Return the courses as JSON
    return json.dumps(courses)


@app.route(f'{api_path}/instructor/edit_grade', methods=['PUT'])
def instructor_edit_grade():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys() or "course_id" not in body.keys() \
            or "student_id" not in body.keys() or "updated_grade" not in body.keys():
        abort(500, description="Information not given!")

    # Attempt to update the student's grade
    result = api.edit_grade(username=body["username"], token=body["token"], course_abbreviation=body["course_id"],
                            student_id=body["student_id"], updated_grade=float(body["updated_grade"]))

    # Return the whether the update was successful
    return json.dumps(f"{{ success: {result} }}")


@app.route(f'{api_path}/admin/sql_statement', methods=['POST'])
def admin_execute_sql():
    # Get the global API context
    api = get_api()

    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys() or \
            "sql_statement" not in body.keys():
        abort(500, description="Information not given!")

    # Attempt to execute the SQL statement (pls no injection :( )
    result = api.execute_sql(username=body["username"], token=body["token"], sql_statement=body["sql_statement"])

    # Return the result of the SQL statement as JSON (might break things!)
    return json.dumps(f"{{ result: {result} }}")


@app.teardown_appcontext
def close_api_context(exception):
    api = getattr(g, "_api", None)
    if api is not None:
        api.close()

    print(f"Exception while tearing down: {exception}") if exception is not None else None


if __name__ == '__main__':
    # Run the app
    app.run()
