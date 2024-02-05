import mysql.connector
from datetime import datetime
from flask import request, render_template

# Configure MariaDB connection
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'admin',
    'database': 'TASKS'
}

def connect_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as error:
        return error

def close_connection(connection):
    if connection:
        connection.close()

def update_task(serial):
    try:
        try:

            connection = connect_db()
            cursor = connection.cursor()    
            query = f"UPDATE tasks SET IsComplete = 'Yes', TasksCompletion= '{datetime.now()}'  WHERE SrNo = '{serial}';" 
            cursor.execute(query,)
            connection.commit()
            cursor.close()
            close_connection(connection)
            return {'returncode': 10, 'message': 'Task Completed!!'}, 200
            
        except Exception as e :
            connection.commit()
            cursor.close()
            close_connection(connection)
            return {'returncode': 1, 'message': f'{e}'}, 503

    except Exception as e:
        cursor.close()
        close_connection(connection)
        return {'returncode': 1, 'message': 'Connection to Available Database was not formed.'}, 503


def add_task():
    try:
        
        # Getting Data Values from User
        data = request.form
        task_name = data['task_name']
        task_description = data['task_description']
        task_type = data['task_type']
    
        # Connecting To DataBase
        connection = connect_db()  
        cursor = connection.cursor()
        try:
            query = "INSERT INTO tasks (TasksCompletion ,TaskName, TaskDescription, TaskType, IsComplete) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (None, task_name, task_description, task_type, "No"))
            connection.commit()
            cursor.close()
            close_connection(connection)
            return '<h1>Task Added!!!</h1>'
        except Exception as e :
            connection.rollback()
            cursor.close()
            close_connection(connection)
            return f'{e}'
    except Exception as e:
        return f'{e}'

def fetch_task():
    try:
        connection = connect_db()  
        cursor = connection.cursor()
        try:
            query = f"SELECT * FROM tasks;"
            cursor.execute(query,)
            rows = cursor.fetchall()
            if rows is not None:
                return render_template('index.html', full_data=rows)
            else:
                connection.rollback()
                cursor.close()
                close_connection(connection)
                return {'returncode': 1, 'message':'No data to be displayed'}, 400
                
        except Exception as e:
            connection.rollback()
            cursor.close()
            close_connection(connection)
            return {'returncode': 1, 'message':f'{e}'}, 503
    except:
        return {'returncode': 1, 'message': 'Connection to Database was not Formed.'}, 503
