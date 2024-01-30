import sqlite3


### ОБЫЧНЫЙ ПОЛЬЗОВАТЕЛЬ
def connect_db_person(new_data): # добавление работяг

    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_client (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT
        )
    ''')

    cursor.execute('SELECT * FROM data_client WHERE name=? AND email=? AND password=?', new_data)
    result = cursor.fetchone()

    if not result:
        cursor.execute('INSERT INTO data_client (name, email, password) VALUES (?, ?, ?)', new_data)
        print('Значения успешно добавлены.')
    else:
        print('Такие значения уже существуют.')

    connect.commit()
    connect.close()


def check_person(person_data): # проверка работяг
    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    query = f"SELECT * FROM data_client WHERE email = ?"
    cursor.execute(query, (person_data[0],))

    result = cursor.fetchone()

    if result:
        query = f"SELECT * FROM data_client WHERE password = ?"
        cursor.execute(query, (person_data[1],))

        result = cursor.fetchone()
        connect.close()

        if result:
            return True
        else:
            return False
    else:
        return False


def check_person_real(person_data): # проверка существование чела
    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    query = f"SELECT * FROM data_client WHERE email = ?"
    cursor.execute(query, (person_data[0],))

    result = cursor.fetchone()

    if result:
        return True
    else:
        return False


def find_client_id_by_email(email): # поиск айди по почте
    connection = sqlite3.connect("data_all.db")
    cursor = connection.cursor()

    try:
        query = "SELECT id FROM data_client WHERE email = ?"
        cursor.execute(query, (email,))

        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    finally:
        connection.close()


def get_all_clients(): # все работяги
    connection = sqlite3.connect("data_all.db")
    cursor = connection.cursor()

    try:
        query = "SELECT email, name FROM data_client"
        cursor.execute(query)

        results = cursor.fetchall()

        need_results = []

        for elem in results:
            need_results.append([elem[0], elem[1]])

        return need_results

    finally:
        connection.close()


### АДМИН

def connect_db_admin(new_data): # добавление админа

    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_admin (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            password TEXT
        )
    ''')

    cursor.execute('SELECT * FROM data_admin WHERE name=? AND email=? AND password=?', new_data)
    result = cursor.fetchone()

    if not result:
        cursor.execute('INSERT INTO data_admin (name, email, password) VALUES (?, ?, ?)', new_data)
        print('Значения успешно добавлены.')
    else:
        print('Такие значения уже существуют.')

    connect.commit()
    connect.close()


def check_admin(person_data): # проверка на админа
    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    query = f"SELECT * FROM data_admin WHERE email = ?"
    cursor.execute(query, (person_data[0],))

    result = cursor.fetchone()

    if result:
        query = f"SELECT * FROM data_admin WHERE password = ?"
        cursor.execute(query, (person_data[1],))

        result = cursor.fetchone()
        connect.close()

        if result:
            return "Салам админ"
        else:
            return "Вы ввели неправильно логин или пароль"
    else:
        connect.close()
        return check_person(person_data)


### ИНФА О ПРИЗАХ

def connect_db_prize(prize_info, client_info): # добавление приза

    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_prize (
            id INTEGER PRIMARY KEY,
            size INTEGER,
            numbers_hits INTEGER,
            name_prize TEXT,
            location_prize TEXT,
            hit_client TEXT
        )
    ''')

    cursor.execute('INSERT INTO data_prize (size, numbers_hits, name_prize, location_prize, hit_client) VALUES (?, ?, ?, ?, ?)', prize_info)

    connect.commit()
    connect.close()

    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS data_client_prize (
                id_client INTEGER,
                id_pole INTEGER
            )
        ''')

    cursor.execute(
        'INSERT INTO data_client_prize (id_client, id_pole) VALUES (?, ?)',
        client_info)

    connect.commit()
    connect.close()


def get_table(id_client): # поиск полей с нужным айди клиента
    connection = sqlite3.connect("data_all.db")
    cursor = connection.cursor()

    try:
        query = "SELECT id_pole FROM data_client_prize WHERE id_client = ?"
        cursor.execute(query, (id_client,))

        result = cursor.fetchall()

        return get_info_table(result)

    finally:
        connection.close()


def get_info_table(id_pole): # выдача инфы о полях для нужного пользователя
    connection = sqlite3.connect("data_all.db")
    cursor = connection.cursor()

    try:
        query = "SELECT id, size, numbers_hits, name_prize, location_prize, hit_client FROM data_prize WHERE id = ?"
        c = 0

        result = []

        while c < len(id_pole):
            cursor.execute(query, (id_pole[c][0],))
            result.append(cursor.fetchone())
            c += 1

        return result

    finally:
        connection.close()


def connect_db_prize_info(prize_info): # добавление инфы о призе

    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_prize_info (
            id INTEGER PRIMARY KEY,
            file TEXT,
            name TEXT,
            description TEXT
        )
    ''')

    cursor.execute('INSERT INTO data_prize_info (file, name, descriptiont) VALUES (?, ?, ?)', prize_info)

    connect.commit()
    connect.close()


def get_dict_prize(): # получение словаря с инфой о призах
    name_db = 'data_all.db'

    connect = sqlite3.connect(name_db)

    cursor = connect.cursor()

    cursor.execute("SELECT id, file, name, description FROM data_prize_info")
    rows = cursor.fetchall()

    data_dict = {}
    for row in rows:
        id, file, name, description = row
        data_dict[id] = [file, name, description]

    connect.close()
    return data_dict
