import datetime
import sqlite3
from typing import List, Tuple, Optional, Dict
import secrets

import nacl.exceptions
from nacl import pwhash, exceptions

from app_structures import AuthenticationToken


class AppAPI(object):
    _db_connection: sqlite3.Connection
    _api_key_size: int
    _global_encoding: str
    _token_duration_hours: int

    def __init__(self, database_path: str):
        self._db_connection = sqlite3.connect(database=database_path)
        self._token_duration_hours = 24
        self._api_key_size = 32
        self._global_encoding = 'utf-8'

    def init_db(self):
        """Initialize the database with the required tables and schemas
        """

        cursor = self._db_connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                username VARCHAR(255) UNIQUE NOT NULL,
                full_name VARCHAR(255),
                password VARCHAR(255) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS access_control (
                access_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                uid INTEGER NOT NULL,
                privilege VARCHAR(255) NOT NULL,
                UNIQUE (uid, privilege),
                CONSTRAINT fk_associated_user FOREIGN KEY (uid) REFERENCES users (uid)
            );
            
            CREATE TABLE IF NOT EXISTS tokens (
                token_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                token_content VARCHAR(255) NOT NULL,
                expiration_datetime VARCHAR(255),
                uid INTEGER NOT NULL,
                CONSTRAINT fk_associated_user FOREIGN KEY (uid) REFERENCES users (uid)
            );
            
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                course_abbreviation VARCHAR(255) NOT NULL,
                course_name VARCHAR(255) NOT NULL,
                instructor_id INTEGER NOT NULL,
                time VARCHAR(255) NOT NULL,
                seats INTEGER NOT NULL,
                CONSTRAINT fk_instructors FOREIGN KEY (instructor_id) REFERENCES users (uid)
            );
            
            CREATE TABLE IF NOT EXISTS enrollment_records (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                uid INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                grade NUMERIC NOT NULL DEFAULT 100.0,
                UNIQUE (uid, course_id),
                CONSTRAINT fk_associated_user FOREIGN KEY (uid) REFERENCES users (uid),
                CONSTRAINT fk_associated_course FOREIGN KEY (course_id) references courses (course_id)
            );
        ''')

    def close(self):
        self._db_connection.close()

    # Helper Functions
    def get_uid(self, username: str) -> str:
        """Get a UID based on a username

        :param username: The username
        :return: A UID associated with the username
        """

        cursor = self._db_connection.cursor()

        # Get UID from the user's username
        cursor.execute('''SELECT uid FROM users WHERE username = ?''', (username,))
        db_result = cursor.fetchone()

        # If the user isn't found
        if db_result is None:
            raise RuntimeError(f"No UID found for username: {username}")

        # Get the user's UID from the returned tuple
        uid = db_result[0]

        return uid

    def get_username(self, uid: str) -> str:
        """Get a username based on a UID

        :param uid: The UID
        :return: A username associated with the UID
        """

        cursor = self._db_connection.cursor()

        # Get username associated with the UID if this UID is in the database
        cursor.execute('''SELECT username FROM users WHERE uid = ?;''', (uid,))
        username = cursor.fetchone()

        # If the user can't be found
        if username is None:
            raise RuntimeError(f"No username found for UID: {uid}")

        # Get the user's username from the returned tuple
        username = username[0]

        return username

    # App Functionality
    def authenticate(self, username: str, password: str) -> Optional[Tuple[AuthenticationToken, List[str]]]:
        """Authenticate User

        :param username: User's username
        :param password: User's password
        :return: Tuple containing an object with the authentication token and the expiration datetime, along with a
                 list of privileges (if success, otherwise None)
        """

        # Verify password using hashed value stored in the DB
        cursor = self._db_connection.cursor()
        cursor.execute('''SELECT uid, password FROM users WHERE username = ?''', (username,))
        db_result = cursor.fetchone()
        if db_result is None:
            print("No matching users found to match password!")
            return None
        uid, password_hash = db_result

        # Actually run verification using NaCl verification function
        try:
            nacl.pwhash.verify(
                password_hash=password_hash,
                password=password.encode(self._global_encoding))
        except nacl.exceptions.InvalidkeyError:
            print("Password failed to verify!")
            return None

        # Get list of privileges from the DB
        cursor.execute('''SELECT privilege FROM access_control WHERE uid = ?''', (uid,))
        db_result = cursor.fetchall()
        privileges = [chunked[0] for chunked in db_result]

        # Generate an authentication token and build the AuthenticationToken object
        token_content = secrets.token_urlsafe(self._api_key_size)
        expiration_datetime = datetime.datetime.now() + datetime.timedelta(hours=self._token_duration_hours)
        authentication_token = AuthenticationToken(token_content=token_content, expiration=expiration_datetime)

        # Store the user's authentication token in the database
        cursor.execute(
            '''INSERT INTO tokens (uid, token_content, expiration_datetime) VALUES (?, ?, ?)''',
            (uid, token_content, str(expiration_datetime))
        )
        self._db_connection.commit()

        # Return values for the API
        return authentication_token, privileges

    def validate(self, username: str, token: str, check_privilege: Optional[str] = None) -> bool:
        """Validate a given user for a given access type

        :param username: The user's username
        :param token: The user's authentication token
        :param check_privilege: (Optional) Access control type to check
        :return: Whether or not the validation was successful
        """
        cursor = self._db_connection.cursor()

        # Get UID from the user's username
        uid = self.get_uid(username=username)

        # Check access control privilege (if specified)
        if check_privilege is not None:
            # Get list of privileges associated with the user (if specified)
            cursor.execute('''SELECT privilege FROM access_control WHERE uid = ?''', (uid,))
            db_result = cursor.fetchall()
            privileges = [chunked[0] for chunked in db_result]

            # If the user does not have the given privilege
            if check_privilege not in privileges:
                return False

        # Get list of tokens associated with a user, if they exist
        cursor.execute(
            '''
            SELECT
                expiration_datetime
            FROM 
                tokens 
            WHERE 
                uid = ? 
            AND 
                token_content = ?
            ORDER BY 
                expiration_datetime
            ;
            ''',
            (uid, token)
        )
        db_result = cursor.fetchone()

        # If there aren't any associate tokens in the DB (the user will need to authenticate first!)
        if db_result is None:
            return False

        # Verify token is not expired
        expiration_datetime = db_result[0]
        if datetime.datetime.fromisoformat(expiration_datetime) < datetime.datetime.now():
            return False
        else:
            return True

    def logout(self, username: str, token: str) -> bool:
        """Invalidate a user's authentication token (log out)

        :param username: User's username
        :param token: User's authentication token (to be invalidated)
        :return: Whether or not the logout was successful
        """

        cursor = self._db_connection.cursor()

        # Get UID from user's username
        uid = self.get_uid(username=username)

        # Remove associated token
        cursor.execute('''DELETE FROM tokens WHERE uid = ? AND token_content = ?''', (uid, token))
        self._db_connection.commit()

        # Return success
        return True

    # Student Activities
    def see_associated_classes(self, username: str, token: str) -> List[Dict[str, object]]:
        """See courses a given student is enrolled in

        :param username: The user's username
        :param token: User's authentication token (will be validated before information is returned)
        :return: List of associated courses as dictionaries
        """

        # Validate user first
        if not self.validate(username=username, token=token, check_privilege='student'):
            raise RuntimeError("User not verified!")

        # Get UID from user's username
        uid = self.get_uid(username=username)

        # Query database for courses associated with this UID
        cursor = self._db_connection.cursor()
        cursor.execute(
            '''
            SELECT 
                courses.course_id,
                courses.course_abbreviation,
                courses.course_name,
                courses.instructor_id, 
                courses.time,
                courses.seats 
            FROM 
                courses 
            INNER JOIN 
                enrollment_records 
            ON 
                courses.course_id = enrollment_records.course_id 
            WHERE 
                enrollment_records.uid = ?
            ;
            ''', (uid,))

        db_results = cursor.fetchall()

        if db_results is None:
            print("No associated courses found!")
            return []

        # Build information dicts for every course this user is enrolled in
        courses = []
        for result in db_results:
            # Get the instructor's username (we don't want to be giving UIDs)
            instructor_name = self.get_username(result[3])

            # Get the number of students enrolled in this course already
            cursor.execute('''SELECT COUNT(*) FROM enrollment_records WHERE course_id = ?;''', (result[0],))
            students_enrolled = cursor.fetchone()[0]
            if students_enrolled is None:
                students_enrolled = 0

            # Build a course dict from the data
            courses.append({
                "course_abbreviation": result[1],
                "course_name": result[2],
                "instructor": instructor_name,
                "time": result[4],
                "students_enrolled": students_enrolled,
                "capacity": result[5],
            })

        return courses

    def see_courses(self, username: str, token: str, spots_available: bool = False) -> List[Dict[str, object]]:
        """See all courses offered by the school

        :param username: The user's username
        :param token: The user's authentication token (will be validated before information is returned)
        :param spots_available: (Optional) Only return courses with free space
        :return: List of courses
        """

        # Validate user first
        if not self.validate(username=username, token=token, check_privilege='student'):
            raise RuntimeError("User not verified!")

        # Query database for all courses
        cursor = self._db_connection.cursor()
        cursor.execute(
            '''
            SELECT 
                course_id,
                course_abbreviation,
                course_name,
                instructor_id, 
                time,
                seats 
            FROM 
                courses
            ;
            ''')
        db_results = cursor.fetchall()

        # If no courses are available
        if db_results is None:
            return []

        # Build information dicts for every course this user is enrolled in
        courses = []
        for result in db_results:
            # Get the instructor's username (we don't want to be giving UIDs)
            instructor_name = self.get_username(result[3])

            # Get the number of students enrolled in this course
            cursor.execute('''SELECT COUNT(*) FROM enrollment_records WHERE course_id = ?;''', (result[0],))
            students_enrolled = cursor.fetchone()[0]
            if students_enrolled is None:
                students_enrolled = 0

            # Don't add if the course is full (BUT ONLY if specified)
            if spots_available and students_enrolled >= result[5]:
                continue

            # Build a course dict from the data
            courses.append({
                "course_abbreviation": result[1],
                "course_name": result[2],
                "instructor": instructor_name,
                "time": result[4],
                "students_enrolled": students_enrolled,
                "capacity": result[5],
            })

        return courses

    def register_for_course(self, username: str, token: str, course_abbreviation: str) -> bool:
        """Register for a given course as the given user

        :param username: The user's username
        :param token: The user's authentication token (will be validated before changes are made)
        :param course_abbreviation: The course to register for (as an abbreviated "identifier")
        :return: Whether or not the registration process was successful
        """

        # Validate user first
        if not self.validate(username=username, token=token, check_privilege='student'):
            raise RuntimeError("User not verified!")

        # Get a DB cursor
        cursor = self._db_connection.cursor()

        # Get UID from user's username
        uid = self.get_uid(username=username)

        # Get the course ID from the course abbreviation
        cursor.execute('''SELECT course_id FROM courses WHERE course_abbreviation LIKE ?''', (course_abbreviation,))
        db_response = cursor.fetchone()

        # If there are no matching course IDs
        if db_response is None:
            return False

        # Extract the course ID from the tuple
        course_id = db_response[0]

        # Attempt to register for the specified course using the database
        cursor.execute('''
            INSERT INTO enrollment_records (uid, course_id) VALUES (?, ?);
        ''', (uid, course_id))
        self._db_connection.commit()

        # Return success
        return True

    # Instructor Activities
    def see_course_students(self, username: str, token: str, course_abbreviation: str) -> List[Tuple[str, float]]:
        """Get list of students and information for a given course

        :param username: The user's username
        :param token: The user's authentication token (will be validated before changes are made)
        :param course_abbreviation: The course to register for (as an abbreviated "identifier")
        :return: List of tuples containing information as (student name, grade)
        """

        # Validate user first
        if not self.validate(username=username, token=token, check_privilege='instructor'):
            raise RuntimeError("User not verified!")

        # Get a DB cursor
        cursor = self._db_connection.cursor()

        # Get the course ID from the abbreviation
        cursor.execute('''
            SELECT course_id FROM courses WHERE course_abbreviation LIKE ?;
        ''', (course_abbreviation,))
        db_result = cursor.fetchone()

        # If no associated courses are found
        if db_result is None:
            RuntimeError(f"Could not find course associated with: {course_abbreviation}")

        # Extract the course ID from the returned tuple
        course_id = db_result[0]

        # Query database for all courses
        cursor.execute(
            '''
            SELECT 
                uid,
                grade
            FROM 
                enrollment_records
            WHERE
                course_id = ?
            ;
            ''', (course_id,))
        db_results = cursor.fetchall()

        # If no courses are available
        if db_results is None or len(db_results) == 0:
            return []

        # Build information dicts for every student enrolled in this course
        students = []
        for result in db_results:
            # Get the student's username (we don't want to be giving UIDs)
            student_name = self.get_username(result[0])

            # Build a course dict from the data
            students.append({
                "name": student_name,
                "grade": float(result[1])
            })

        # Return list of student info dictionaries
        return students

    def see_teaching_courses(self, username: str, token: str) -> List[Dict[str, object]]:
        """See courses a given instructor is teaching

        :param username: The user's username
        :param token: User's authentication token (will be validated before information is returned)
        :return: List of associated courses as dictionaries
        """

        # Validate user first
        if not self.validate(username=username, token=token, check_privilege='instructor'):
            raise RuntimeError("User not verified!")

        # Get UID from user's username
        uid = self.get_uid(username=username)

        # Query database for courses instructed by a user with this UID
        cursor = self._db_connection.cursor()
        cursor.execute(
            '''
            SELECT 
                course_id,
                course_abbreviation,
                course_name, 
                time,
                seats 
            FROM 
                courses
            WHERE 
                instructor_id = ?
            ;
            ''', (uid,))

        db_results = cursor.fetchall()

        if db_results is None:
            print("No associated courses found!")
            return []

        # Build information dicts for every course this user is instructing
        courses = []
        for result in db_results:
            # Get the number of students enrolled in this course already
            cursor.execute('''SELECT COUNT(*) FROM enrollment_records WHERE course_id = ?;''', (result[0],))
            students_enrolled = cursor.fetchone()[0]
            if students_enrolled is None:
                students_enrolled = 0

            # Build a course dict from the data
            courses.append({
                "course_abbreviation": result[1],
                "course_name": result[2],
                "time": result[3],
                "students_enrolled": students_enrolled,
                "capacity": result[4],
            })

        return courses

    def edit_grade(self, username: str, token: str, course_abbreviation: str, student_id: str, updated_grade: float) -> bool:
        """Edit a student's grade for a given course

        :param username: The user's username
        :param token: The user's authentication token (will be validated before changes are made)
        :param course_abbreviation: The course to register for (as an abbreviated "identifier")
        :param student_id: The student's student ID (to change)
        :param updated_grade: The updated grade for the student
        """

        # Validate user first
        if not self.validate(username=username, token=token, check_privilege='instructor'):
            raise RuntimeError("User not verified!")

        # Get the student's UID
        student_uid = self.get_uid(username=student_id)

        # Get a DB cursor
        cursor = self._db_connection.cursor()

        # Get the course ID from the abbreviation
        cursor.execute('''
                    SELECT course_id FROM courses WHERE course_abbreviation LIKE ?;
                ''', (course_abbreviation,))
        db_result = cursor.fetchone()

        # If no associated courses are found
        if db_result is None:
            RuntimeError(f"Could not find course associated with: {course_abbreviation}")

        # Extract the course ID from the returned tuple
        course_id = db_result[0]

        # Run update in the DB
        cursor.execute('''
            UPDATE enrollment_records SET grade = ? WHERE uid = ? AND course_id = ?
        ''', (updated_grade, student_uid, course_id))
        self._db_connection.commit()

        return True

    # Admin Activities

    def execute_sql(self, username: str, token: str, sql_statement: str) -> Optional[str]:
        """Execute a raw SQL statement in the database

        :param username: The user's username
        :param token: The user's authentication token (will be validated before changes are made)
        :param sql_statement: The statement to execute in the database
        """

        # Validate user first
        if not self.validate(username=username, token=token, check_privilege='admin'):
            raise RuntimeError("User not verified!")

        # Run the SQL
        cursor = self._db_connection.cursor()
        cursor.execute(sql_statement)

        # Finalize
        db_result = cursor.fetchall()
        self._db_connection.commit()

        # Return as string
        return str(db_result)
