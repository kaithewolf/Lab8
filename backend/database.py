import sqlite3


def get_all_of_role(db_connection, user_role):
    command = '''
    SELECT 
        * 
    FROM 
        Users
    WHERE 
        u_role = ?
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command, str(user_role))
    result = db_cursor.fetchall()
    print(result)
    return result


def get_all_classes(db_connection):
    command = '''
    SELECT 
        * 
    FROM 
        Classes
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command)
    result = db_cursor.fetchall()
    print(result)
    return result


def get_all_users(db_connection):
    command = '''
    SELECT 
        * 
    FROM 
        Users
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command)
    result = db_cursor.fetchall()
    print(result)
    return result


def get_user(user, db_connection):
    command = '''
    SELECT 
        * 
    FROM 
        Users 
    WHERE 
        u_name = ?
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command, user)
    result = db_cursor.fetchone()
    return result


def get_classes_of_student(db_connection, user):
    command = '''
    SELECT 
        c_classname, 
        c_teacher, 
        c_time, 
        c_seats
    FROM 
        Classes, 
        Students_in_Classes
    WHERE 
        sc_name = ?
    AND 
        sc_classkey = c_classkey
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command, user)
    result = db_cursor.fetchall()
    print(result)
    return result


def get_classes_of_teacher(db_connection, user):
    command = '''
    SELECT 
        c_classkey, 
        c_classname, 
        c_teacher, 
        c_time, 
        c_seats
    FROM 
        Classes
    WHERE 
        c_teacher = ?
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command, user)
    result = db_cursor.fetchall()
    print(result)
    return result


def get_students_in_classes(db_connection):
    command = '''
    SELECT 
        * 
    FROM
        Students_in_CLasses
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command)
    result = db_cursor.fetchall()
    print(result)
    return result


def get_students_in_a_class(db_connection, class_key):
    command = '''
    SELECT 
        sc_name, 
        sc_grade
    FROM 
        Students_in_Classes
    WHERE 
        sc_classkey = ?
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command, str(class_key))
    result = db_cursor.fetchall()
    print(result)
    return result


def create_db(db_connection):
    command = '''
    CREATE TABLE Users (
        u_name varchar(255) primary key not null,
        u_password varchar(255) not null,
        u_role varchar(1) not null
    );
    '''
    db_connection.execute(command)

    command = '''
    CREATE TABLE Classes (
        c_classkey int primary key not null,
        c_classname varchar(255) DEFAULT "TBA" not null,
        c_teacher varchar(255) DEFAULT "TBA" not null,
        c_time varchar(255) DEFAULT "TBA" not null,
        c_seats int not null
    );   
    '''
    db_connection.execute(command)

    command = '''
    CREATE TABLE Students_in_Classes (
        sc_classkey int not null,
        sc_name varchar(255) not null,
        sc_grade int not null,
        primary key (sc_classkey, sc_name)
    )
    '''
    db_connection.execute(command)
    db_connection.commit()


def insert_user(db_connection, name, password, user_type):
    command = '''
    INSERT INTO
        Users
    VALUES(?, ?, ?)
    ;
    '''

    db_connection.execute(command, str(name), str(password), str(user_type))
    db_connection.commit()


def delete_user(db_connection, name):
    get_result = get_user(name, db_connection)

    if get_result is not None:
        user_type = get_result[2]
        command = "DELETE FROM Users WHERE u_name = ?;"
        db_connection.execute(command, name)
        db_connection.commit()
        if user_type == "s":
            command = "DELETE FROM Students_in_Classes WHERE sc_name = ?;"
            db_connection.execute(command, name)
            db_connection.commit()

        elif user_type == "t":
            command = "UPDATE Classes SET c_teacher = \"TBA\" WHERE c_teacher = ?;"
            db_connection.execute(command, name)
            db_connection.commit()
    else:
        # [TODO] DB errors need to be returned, not just printed!
        print("ERROR: User not found\n")


def student_add_class(db_connection, name, class_key):
    command = '''
    INSERT INTO
        Students_in_Classes
    VALUES (?, ?, ?)
    ;
    '''
    db_connection.execute(command, str(class_key), str(name), 100)
    db_connection.commit()


def student_drop_class(db_connection, name, class_key):
    command = '''
    DELETE FROM
        Students_in_Classes
    WHERE
        sc_name = ?
    AND
        sc_classkey = ?
    ;
    '''

    db_connection.execute(command, str(name), str(class_key))
    db_connection.commit()


def insert_class(db_connection, key, name, teacher, time, seats):
    command = '''
    INSERT INTO
        Classes
    VALUES (?, ?, ?, ?, ?)
    ;
    '''

    db_connection.execute(command, str(key), str(name), str(teacher), str(time), str(seats))
    db_connection.commit()


def student_grades_in_student_class(db_connection, name):
    command = '''
    SELECT
        c_classname,
        sc_grade
    FROM
        Students_in_Classes,
        Classes
    WHERE
        sc_name = ?
    AND
        sc_classkey = c_classkey
    ;
    '''

    db_cursor = db_connection.cursor()
    db_cursor.execute(command, str(name))
    result = db_cursor.fetchall()
    print(result)
    return result


def edit_student_grade(db_connection, student_name, class_key, grade):
    command = '''
    UPDATE
        Students_in_Classes
    SET 
        sc_grade = ?,
    WHERE 
        sc_name = ?
    AND
        sc_classkey = ?
    ;
    '''

    db_connection.execute(command, str(grade), str(student_name), str(class_key))
    db_connection.commit()
