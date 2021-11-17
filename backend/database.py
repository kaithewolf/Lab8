from ast import get_docstring
import sqlite3

def get_all_of_role(c, role):
    command = '''
    SELECT * FROM Users
    WHERE u_role = \"''' + str(role) +'''\" ;
    '''

    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchall()
    print(result)
    return result

def get_all_classes(c):
    command = '''
    SELECT * FROM Classes
    '''
    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchall()
    print(result)
    return result

def get_all_users(c):
    command = '''
    SELECT * FROM Users
    '''
    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchall()
    print(result)
    return result

def get_user(user, c):
    command = '''
    SELECT * FROM Users WHERE u_name =''' + "\""+ user +"\"" +";"
    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchone()
    return result

def get_classes_of_student(c, user):
    command = '''
    SELECT c_classname, c_teacher, c_time, c_seats
    FROM Classes, Students_in_Classes
    WHERE sc_name = \"''' + user + '''\"
    and sc_classkey = c_classkey
    '''
    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchall()
    print(result)
    return result

def get_classes_of_teacher(c, user):
    command = '''
    SELECT c_classkey, c_classname, c_teacher, c_time, c_seats
    FROM Classes
    WHERE c_teacher = \"''' + user + '''\"'''
    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchall()
    print(result)
    return result

def get_students_in_classes(c):
    command = '''
    SELECT * FROM Students_in_CLasses
    '''
    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchall()
    print(result)
    return result

def get_students_in_a_class(classkey, c):
    command = '''
    SELECT sc_name, sc_grade
    FROM Students_in_Classes
    WHERE sc_classkey = ''' + str(classkey)
    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchall()
    print(result)
    return result

def create_db(c):
    command = '''
    CREATE TABLE Users (
        u_name varchar(255) primary key not null,
        u_password varchar(255) not null,
        u_role varchar(1) not null
    );
    '''
    c.execute(command)

    command = '''
    CREATE TABLE Classes (
        c_classkey int primary key not null,
        c_classname varchar(255) DEFAULT "TBA" not null,
        c_teacher varchar(255) DEFAULT "TBA" not null,
        c_time varchar(255) DEFAULT "TBA" not null,
        c_seats int not null
    );   
    '''
    c.execute(command)

    command = '''
    CREATE TABLE Students_in_Classes (
        sc_classkey int not null,
        sc_name varchar(255) not null,
        sc_grade int not null,
        primary key (sc_classkey, sc_name)
    )
    '''
    c.execute(command)
    c.commit()

def insert_user(name, password, type, c):
    command = '''
    INSERT INTO Users
    values('''+\
    "\""+str(name)+"\", "+\
    "\""+str(password)+"\", "+\
    "\""+str(type)+"\");"
    
    c.execute(command)
    c.commit()

def delete_user(name, c):
    get_result = get_user(name, c)

    if get_result != None:
        user_type = get_result[2]
        command = "DELETE FROM Users WHERE u_name = \""+name+"\";"
        c.execute(command)
        c.commit()
        if user_type == "s":
            command = "DELETE FROM Students_in_Classes WHERE sc_name = \""+name+"\";"
            c.execute(command)
            c.commit()
        
        elif user_type == "t":
            command = "UPDATE Classes SET c_teacher = \"TBA\" WHERE c_teacher = \""+name+"\";"
            c.execute(command)
            c.commit()
    else:
        print("ERROR: User not found\n")
    
    
def student_add_class(name, classkey, c):
    command = '''
    INSERT INTO Students_in_Classes
    values('''+str(classkey)+\
    ", \""+str(name)+"\", 100);"
    c.execute(command)
    c.commit()

def student_drop_class(name, classkey, c):
    command = '''
    DELETE FROM Students_in_Classes '''+\
    "WHERE sc_name = \""+str(name)+"\"and sc_classkey = "+str(classkey)+";"
    c.execute(command)
    c.commit()

def insert_class(key, name, teacher, time, seats, c):
    command = '''
    INSERT INTO Classes
    values('''+str(key)+", "+\
    "\""+str(name)+"\", "+\
    "\""+str(teacher)+"\", "+\
    "\""+str(time)+"\", "+str(seats)+");"
    
    c.execute(command)
    c.commit()

def student_grades_in_student_class(name, c):
    command = '''
    SELECT c_classname, sc_grade
    FROM Students_in_Classes, Classes '''+\
    "WHERE sc_name = \""+str(name)+"\" and sc_classkey = c_classkey"
    cur = c.cursor()
    cur.execute(command)
    result = cur.fetchall()
    print(result)
    return result

def edit_student_grade(student_name, classkey, grade, c):
    command = "UPDATE Students_in_Classes "+\
    "SET sc_grade = "+str(grade)+" "+\
    "WHERE sc_name = \""+str(student_name)+"\" and sc_classkey = "+str(classkey)+";"
    c.execute(command)
    c.commit()
    

""" ''if __name__ == '__main__':
    _conn = sqlite3.connect(":memory:")
    cur = _conn.cursor()
    create_db(_conn)

    insert_user("jonny sucffed", "123456", "s", _conn)
    insert_user("binyi chen", "hollaback", "s", _conn)
    insert_user("angelo kyrilov", "good password", "t", _conn)
    insert_user("admin", "admin", "a", _conn)
    insert_user("daniel leung", "hi1000", "t", _conn)

    insert_class(1, "CSE-106", "angelo kyrilov", "1:30-2:45", 130, _conn)
    insert_class(2, "CSE-031", "daniel leung", "12:00-1:15", 130, _conn)
    insert_class(3, "ENGR-065", "angelo kyrilov", "10:30-11:45", 100, _conn)

    student_add_class("binyi chen", 1, _conn)
    student_add_class("binyi chen", 2, _conn)
    student_add_class("jonny sucffed", 2, _conn)

    edit_student_grade("binyi chen", 1, 70, _conn)
    edit_student_grade("binyi chen", 2, 60, _conn)

    student_grades_in_student_class("binyi chen", _conn)
    get_students_in_a_class(2, _conn)

    get_classes_of_teacher(_conn, "angelo kyrilov")
    
    delete_user("daniel leung", _conn)
    get_all_classes(_conn)'' """