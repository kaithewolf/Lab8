from datetime import datetime
from typing import Optional


class AuthenticationToken(object):
    token_content: str
    expiration: Optional[datetime]

    def __init__(self, token_content: str, expiration: Optional[datetime]) -> None:
        self.token_content = token_content
        self.expiration = expiration

    def is_expired(self) -> bool:

        # Check if the authentication token actually exists
        if self.token_content is None:
            return True

        # Check if the authentication token is expired
        if datetime.now() > self.expiration:
            return True

        # Otherwise, token _is not_ expired
        return False


class Course(object):
    course_id: str
    course_name: str
    instructor: str
    time: str
    students_enrolled: int
    capacity: int

    def __init__(self, course_id: str, course_name: str, instructor: str, time: str, students_enrolled: int,
                 capacity: int) -> None:
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.time = time
        self.students_enrolled = students_enrolled
        self.capacity = capacity
