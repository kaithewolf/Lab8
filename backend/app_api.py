from typing import List, Tuple, Optional

from app_structures import AuthenticationToken, Course


# App Functionality
def authenticate(username: str, password: str) -> AuthenticationToken:
    """Authenticate User

    :param username: User's username
    :param password: User's password
    :return: Object containing the authentication token and the expiration datetime
    """
    pass


def validate(username: str, token: str, access_type: str) -> bool:
    """Validate a given user for a given access type

    :param username: The user's username
    :param token: The user's authentication token
    :param access_type: Access control type to check
    :return: Whether or not the validation was successful
    """
    pass


def logout(username: str, token: str) -> bool:
    """Invalidate a user's authentication token (log out)

    :param username: User's username
    :param token: User's authentication token (to be invalidated)
    :return: Whether or not the logout was successful
    """
    pass


# Student Activities
def see_associated_classes(username: str, token: str, student_name: str) -> List[Course]:
    """See courses a given student is associated with

    :param username: The user's username
    :param token: User's authentication token (will be validated before information is returned)
    :param student_name: Student's name as recorded in the system (non-fuzzy)
    :return: List of associated courses as Course objects
    """
    pass


def see_courses(username: str, token: str, spots_available: bool = False) -> List[Course]:
    """See all courses offered by the school

    :param username: The user's username
    :param token: The user's authentication token (will be validated before information is returned)
    :param spots_available: (Optional) Only return courses with free space
    :return: List of courses
    """
    pass


def register_for_course(username: str, token: str, course_id: str) -> bool:
    """Register for a given course as the given user

    :param username: The user's username
    :param token: The user's authentication token (will be validated before changes are made)
    :param course_id: The course ID to register for
    :return: Whether or not the registration process was successful
    """
    pass


# Instructor Activities
def see_course_students(username: str, token: str, course_id: str) -> List[Tuple[str, float]]:
    """Get list of students and information for a given course

    :param username: The user's username
    :param token: The user's authentication token (will be validated before changes are made)
    :param course_id: The course ID to view
    :return: List of tuples containing information as (student name, grade)
    """
    pass


def edit_grade(username: str, token: str, course_id: str, student_id: str, updated_grade: float) -> bool:
    """Edit a student's grade for a given course

    :param username: The user's username
    :param token: The user's authentication token (will be validated before changes are made)
    :param course_id: The course identifier
    :param student_id: The student's student ID (to change)
    :param updated_grade: The updated grade for the student
    """
    pass


# Admin Activities

def execute_sql(username: str, token: str, sql_statement: str) -> Optional[str]:
    """Execute a raw SQL statement in the database

    :param username: The user's username
    :param token: The user's authentication token (will be validated before changes are made)
    :param sql_statement: The statement to execute in the database
    """
    pass
