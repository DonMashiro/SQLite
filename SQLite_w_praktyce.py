import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    return rows

def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows

def delete_where(conn, table, **kwargs):
    """
    Delete from table where attributes from kwargs.
    :param conn: Connection to the SQLite database
    :param table: table name
    :param kwargs: dict of attributes and values
    :return:
    """
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    
def update(conn, table, name, **kwargs):
    """
    Update number of repetitions of the exercise
    :param conn: the Connection object
    :param table: table name
    :param name: name of the exercise to update
    :return:
    """
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (name, )

    sql = f''' UPDATE {table}
               SET {parameters}
               WHERE name = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Error updating record: {e}")

def create_tables(conn):
    create_trainings_sql = """
    -- trainings table
    CREATE TABLE IF NOT EXISTS trainings (
       id integer PRIMARY KEY,
       body_part text NOT NULL,
       start_date text,
       end_date text
    );
    """

    create_exercises_sql = """
    -- exercises table
    CREATE TABLE IF NOT EXISTS exercises (
       id integer PRIMARY KEY,
       training_id integer NOT NULL,
       name VARCHAR(250) NOT NULL,
       number_of_series numeric NOT NULL,
       number_of_rep numeric NOT NULL,
       status VARCHAR(15) NOT NULL,
       start_date text NOT NULL,
       end_date text NOT NULL,
       FOREIGN KEY (training_id) REFERENCES trainings (id)
    );
    """
    
    execute_sql(conn, create_trainings_sql)
    execute_sql(conn, create_exercises_sql)

def add_training(conn, training):
    """
    Create a new training into the trainings table
    :param conn:
    :param training: 
    :return: training id
    """
    sql = ''' INSERT INTO trainings(body_part, start_date, end_date)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, training)
    conn.commit()
    return cur.lastrowid

def add_exercise(conn, exercise):
    """
    Create a new exercise into the exercises table
    :param conn:
    :param exercise: 
    :return: exercise id
    """
    sql = ''' INSERT INTO exercises(training_id, name, number_of_series, number_of_rep, status, start_date, end_date)
              VALUES(?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, exercise)
    conn.commit()
    return cur.lastrowid

if __name__ == "__main__":
    conn = create_connection("database.db")
    
    create_tables(conn)
    
    training = ("biceps", "2024-09-20 10:00:00", "2024-09-20 12:00:00")
    tr_id = add_training(conn, training)

    exercises = [
        (tr_id, "cable curls", 4, 12, "finished", "2024-09-20 10:00:00", "2024-09-20 10:30:00"),
        (tr_id, "hammer curls", 4, 12, "finished", "2024-09-20 10:35:00", "2024-09-20 11:00:00"),
        (tr_id, "EZ-Bar Curl", 4, 12, "finished", "2024-09-20 11:05:00", "2024-09-20 11:30:00"),
        (tr_id, "chin up", 3, 15, "ongoing", "2024-09-20 11:35:00", "2024-09-20 12:00:00")
    ]
    
    for exercise in exercises:
        exercise_id = add_exercise(conn, exercise)
    
    #Update number of repetitions of the exercise 'EZ-Bar Curl' from 12 to 15
    update(conn, "exercises", "EZ-Bar Curl", number_of_rep=15)

    #Delete the exercise 'chin up' directly
    delete_where(conn, "exercises", name="chin up")

    print("All exercises:")
    all_exercises = select_all(conn, "exercises")
    for row in all_exercises:
        print(row)
    
    conn.close()
