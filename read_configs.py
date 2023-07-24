import sqlite3 as sql

class ctrl:

    def __init__(self, path):
        self.path = path

    def sql_init(self):
        with sql.connect(self.path) as connect:
            cursor = connect.cursor()

            # cursor.execute("""DROP TABLE IF EXISTS data""")
            cursor.execute('''CREATE TABLE IF NOT EXISTS events(
                id INTEGER NOT NULL UNIQUE,
                name TEXT NOT NULL,
                text TEXT NOT NULL,  
                date TEXT NOT NULL,
                PRIMARY KEY(id AUTOINCREMENT)
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins(
                id INTEGER INTEGER NOT NULL UNIQUE,
                id_tg INTEGER,
                PRIMARY KEY(id AUTOINCREMENT) 
            );
            ''')

    def getAdmin(self, ids):
        with sql.connect(self.path) as connect:
            cursor = connect.cursor()
            cursor.execute(f'SELECT * FROM admins WHERE id_tg = {ids};')
            id_tg = cursor.fetchone()
            return id_tg

    def getAdmins(self):
        data = []
        with sql.connect(self.path) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM admins;')
            ids_and_status = cursor.fetchall()
            for info in ids_and_status:
                info = str(info).replace('(', '').replace(')', '').replace("'", '').split(', ')
                data.append(
                    {
                        "id": info[0],
                        "id_tg": info[1],
                    }
                )

        return data

    def getEvents(self):
        data = []
        with sql.connect(self.path) as connect:
            cursor = connect.cursor()
            cursor.execute('SELECT * FROM events;')
            ids_and_status = cursor.fetchall()
            # print(ids_and_status)
            for info in ids_and_status:
                # info = str(info).replace('(', '').replace(')', '').replace("'", '').split(', ')
                data.append(
                    {
                        "id": info[0],
                        "name": info[1],
                        "text": info[2],
                        "date": info[3],

                    }
                )

        return data

    def setEvent(self, dto):
        with sql.connect(self.path) as connect:
            cursor = connect.cursor()
            event = (dto["name"], dto["text"], dto["date"])
            cursor.execute(f'INSERT INTO events (name, text, date) VALUES(?,?,?);', event)

    def setAdmin(self, id_tg):
        with sql.connect(self.path) as connect:
            cursor = connect.cursor()
            cursor.execute(f'INSERT INTO admins (id_tg) VALUES({id_tg});')
