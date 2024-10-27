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

if __name__ == "__main__":

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
    
   db_file = "database_2.db"

   conn = create_connection(db_file)
   if conn is not None:
       execute_sql(conn, create_trainings_sql)
       execute_sql(conn, create_exercises_sql)
       conn.close()

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
    training = ("biceps", "2024-09-20 10:00:00", "2024-09-20 11:30:00")
    
    conn = create_connection("database_2.db")
    tr_id = add_training(conn, training)

    exercise = (tr_id,
                "cable curls",
                4,
                12, 
                "finished",
                "2024-09-20 10:00:00",
                "2024-09-20 10:30:00"
    )
    
    exercise_id = add_exercise(conn, exercise)
    
    print(tr_id, exercise_id)
    conn.commit()