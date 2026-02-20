import sqlite3
db_name = 'quiz.sqlite'
conn = None
curor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' delete all tables '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

    
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')

    do('''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR)'''
        )

    do(
        '''CREATE TABLE IF NOT EXISTS question(
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,                         
        wrong1 VARCHAR,                         
        wrong2 VARCHAR,
        wrong3 VARCHAR
        )'''
    )

    do(
        '''CREATE TABLE IF NOT EXISTS quiz_content(
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY(quiz_id) REFERENCES quiz(id),
        FOREIGN KEY(question_id) REFERENCES question(id)
        )'''
    )           

    close()

def add_questions():
    questions = [
        ('80+31+21+90+34+64+91+32=', '353', 'gak tahu', '1 juta','infiniti'),
        ('523x253', '132.319', 'gak tahu', '1 juta','infiniti'),
        ('apa arti M dalam angka romawi', 'seribu', 'gak tahu', '1 juta','infiniti'),
        ('1/0?', 'tidak terdef', 'gak tahu', '1 juta','infiniti'),
        ('roblox adalah?', 'platform', 'game', 'blox fruit', 'brookhaven'),
        ('apa benda yang lebih kecil daripada atom?', 'proton,neutron,dan elektron', 'gak ada', 'ya mana saya tau', 'ntah'),
        ('diantara proton,neutron,dan elektron manakah yang menghasilkan listrik?', 'elektron', 'neutron', 'proton','Air'),
        ('apa nama galaksi kita', 'bima sakti', 'ya mana saya tau', 'dipikir saya enstein?', 'bima galak'),
        ('siapa yang membuat lukisan monalisa', 'leonardo dafinci','adalah','parasut', 'mana saya tau'),
        ('macbook berasal dari merek?', 'apple','iphone','android', 'mana saya tau'),
        ('iphone berasak dari merek?', 'apple','macbook','android', 'mana saya tau'),
        ('75+25?', '100','macbook','android', 'mana saya tau'),
        ('jika terkena sentruman listrik tetapi hanya terkena + nya saja maka apa yang akan terjadi?', 'tidak kenapa-napa','kesetrumlah!','logika kocak ya kesetrumlah', 'mikir! jelas-jelas pasti kesetrum!')
    ]

    open()
    cursor.executemany(
        '''INSERT INTO question(question, answer, wrong1, wrong2, wrong3) VALUES(?, ?, ?, ?, ?);''', questions
    )
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('angka', ),
        ('game', ),
        ('atom', )
    ]
    open()
    cursor.executemany(
        '''INSERT INTO quiz(name) VALUES(?);''', quizes
    )
    conn.commit()
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def show_question_list():
    open()
    cursor.execute("SELECT id, question FROM question")
    print("\n=== LIST QUESTION ===")
    for row in cursor.fetchall():
        print(f"{row[0]}. {row[1]}")
    close()

def show_quiz_list():
    open()
    cursor.execute("SELECT id, name FROM quiz")
    print("\n=== LIST QUIZ ===")
    for row in cursor.fetchall():
        print(f"{row[0]}. {row[1]}")
    close()

def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?, ?)"
    # answer = input("Add a link (y/n)")
    # while answer != 'n':
    #     quiz_id = int(input("quiz id: "))
    #     question_id = int(input("question id: "))
    #     cursor.execute(query, [quiz_id, question_id])
    #     conn.commit()
    #     answer = input("Add a link (y/n)")
    cursor.execute(query, (1, 1))
    cursor.execute(query, (1, 2))
    cursor.execute(query, (1, 3))
    cursor.execute(query, (1, 4))
    cursor.execute(query, (2, 5))
    cursor.execute(query, (3, 6))
    cursor.execute(query, (3, 7)) 
    cursor.execute(query, (3, 8)) 
    cursor.execute(query, (3, 9)) 
    cursor.execute(query, (2, 10)) 
    cursor.execute(query, (2, 11)) 
    cursor.execute(query, (1, 12)) 
    cursor.execute(query, (3, 13)) 
    close()
def get_quises():
    open()
    cursor.execute('SELECT id, name FROM quiz ORDER BY id')
    result = cursor.fetchall()
    close()
    return result

def get_question_after(question_id = 0, quiz_id = 1):
  open()
  query = '''
  SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3

  FROM question, quiz_content

  WHERE quiz_content.question_id == question.id
  AND quiz_content.id > ? AND quiz_content.quiz_id == ?
  ORDER BY quiz_content.id
  '''
  cursor.execute(query, [question_id, quiz_id])
  result = cursor.fetchone()
  close()
  return result

def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    
    # show_quiz_list()
    # show_question_list()
    
    add_links()
    show_tables()
    # print(get_question_after(3, 1))

if __name__ == "__main__":
    main()
