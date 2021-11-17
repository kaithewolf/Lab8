import json

from flask import Flask, request, abort

from backend.app_api import authenticate, logout, see_associated_classes, see_courses, register_for_course, \
    see_course_students, edit_grade, execute_sql

app = Flask(__name__)

# Configuration variables
api_path = "/api/v1"


# Base application routers
@app.route('/')
def home_handler():
    return 'Please use the API at /api/v1/!'


@app.route(f'{api_path}/auth/', methods=['POST'])
def api_auth():
    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "password" not in body.keys():
        abort(401, description="Information not given!")

    # Attempt to authenticate the user
    auth_token = authenticate(username=body["username"], password=body["password"])

    # Verify authentication was successful
    if auth_token is None:
        abort(401, description="Could not authorize!")

    # Build response and return information
    response = f"{{ \"auth_token\": \"{auth_token.token_content}\", \"expiration\": \"{auth_token.expiration}\" }}"
    return json.loads(response)


@app.route(f'{api_path}/auth/logout', methods=['POST'])
def api_logout():
    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys():
        abort(500, description="Information not given!")

    # Perform logout
    result = logout(username=body["username"], token=body["token"])

    # Return the status
    return f"{{ success: {result} }}"


# Student application routers
@app.route(f'{api_path}/student/my_courses', methods=['GET'])
def student_my_courses():
    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys():
        abort(500, description="Information not given!")

    # Get student's courses
    # [TODO] Change student_name to the actual student's name
    courses = see_associated_classes(username=body["username"], token=body["token"], student_name=body["username"])

    # Return the courses as JSON
    return json.dumps(courses)


@app.route(f'{api_path}/student/all_courses', methods=['GET'])
def student_all_courses():
    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys():
        abort(500, description="Information not given!")

    # Get list of courses + course info
    courses = see_courses(username=body["username"], token=body["token"], spots_available=False)

    # Return the courses as JSON
    return json.dumps(courses)


@app.route(f'{api_path}/student/register_course', methods=['POST'])
def student_register_course():
    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys() and "course_id" not in body.keys():
        abort(500, description="Information not given!")

    # Get list of courses + course info
    result = register_for_course(username=body["username"], token=body["token"], course_id=body["course_id"])

    # Return the whether the registration was successful
    return json.dumps(f"{{ success: {result} }}")


# Instructor application routers
@app.route(f'{api_path}/instructor/course_students', methods=['GET'])
def instructor_get_students():
    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys() or "course_id" not in body.keys():
        abort(500, description="Information not given!")

    # Get list of students as tuples
    course_students = see_course_students(username=body["username"], token=body["token"], course_id=body["course_id"])

    # Return the students as JSON
    return json.dumps(course_students)


@app.route(f'{api_path}/instructor/edit_grade', methods=['PUT'])
def instructor_edit_grade():
    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys() or "course_id" not in body.keys() \
            or "student_id" not in body.keys() or "updated_grade" not in body.keys():
        abort(500, description="Information not given!")

    # Attempt to update the student's grade
    result = edit_grade(username=body["username"], token=body["token"], course_id=body["course_id"],
                        student_id=body["student_id"], updated_grade=float(body["updated_grade"]))

    # Return the whether the update was successful
    return json.dumps(f"{{ success: {result} }}")


@app.route(f'{api_path}/admin/sql_statement', methods=['POST'])
def admin_execute_sql():
    body = request.json

    # Verify correct parameters have been given
    if body is None or "username" not in body.keys() or "token" not in body.keys() or \
            "sql_statement" not in body.keys():
        abort(500, description="Information not given!")

    # Attempt to execute the SQL statement (pls no injection :( )
    result = execute_sql(username=body["username"], token=body["token"], sql_statement=body["sql_statement"])

    # Return the result of the SQL statement as JSON (might break things!)
    return json.dumps(f"{{ result: {result} }}")


if __name__ == '__main__':

    # Run the app
    app.run()
