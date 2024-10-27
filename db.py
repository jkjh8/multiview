import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS setup (id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT, value_int INTEGER, value_string text, value_bool BOOLEAN)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS player (player INTEGER PRIMARY KEY, mrl INTEGER, status STRING)")
        self.conn.commit()

    def insert(self, key, value):
        if (type(value) == int):
            self.cur.execute("INSERT INTO setup VALUES (NULL, ?, ?, NULL, NULL)", (key, value))
        elif (type(value) == str):
            self.cur.execute("INSERT INTO setup VALUES (NULL, ?, NULL, ?, NULL)", (key, value))
        elif (type(value) == bool):
            self.cur.execute("INSERT INTO setup VALUES (NULL, ?, NULL, NULL, ?)", (key, value))
        self.conn.commit()

    def view(self, table="setup"):
        self.cur.execute(f"SELECT * FROM {table}")
        rows = self.cur.fetchall()
        return self.rt_object(rows)

    def search(self, key="", value_int="", value_string="", value_bool=""):
        self.cur.execute("SELECT * FROM setup WHERE key=? OR author=? OR year=? OR isbn=?", (key, value_int, value_string, value_bool))
        rows = self.cur.fetchall()
        return self.rt_object(rows)

    def rt_object(self, rows):
        rows_dict = []
        for row in rows:
            row_dict = {
            "id": row[0],
            "key": row[1],
            "value": row[2] if row[2] is not None else (row[3] if row[3] is not None else row[4])
            }
            rows_dict.append(row_dict)
        return rows_dict

    def delete(self, id):
        self.cur.execute("DELETE FROM setup WHERE id=?", (id,))
        self.conn.commit()

    def update(self, key, value):
        if (type(value) == int):
            self.cur.execute("UPDATE setup SET value_int=? WHERE key=?", (value, key))
        elif (type(value) == str):
            self.cur.execute("UPDATE setup SET value_string=? WHERE key=?", (value, key))
        elif (type(value) == bool):
            self.cur.execute("UPDATE setup SET value_bool=? WHERE key=?", (value, key))
        self.conn.commit()
        
    def drop_table(self, table):
        self.cur.execute("DROP TABLE IF EXISTS "+table)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
        