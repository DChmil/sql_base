import psycopg2
from psycopg2.sql import SQL, Identifier

def add_client(con, first_name, last_name, email, phones=None):
    con.execute("""
                INSERT INTO client(name, surname, email) VALUES(%s, %s, %s) RETURNING id;
                """, (first_name, last_name, email))
    conn.commit()
    for phone in phones:
        nomber = add_phone(con, con.fetchone()[0], phone)
    return

def add_phone(con, client_id, phone):
    con.execute("""
                            INSERT INTO contact(client_id, number) VALUES(%s, %s) RETURNING client_id;
                            """, (client_id, phone))
    conn.commit()
    return

def change_client(con, client_id, first_name=None, last_name=None, email=None):
    client_list = {'name': first_name, "surname": last_name, 'email': email}
    for key, arg in client_list.items():
        if arg:
            con.execute(SQL("UPDATE Client SET {}=%s WHERE id=%s").format(Identifier(key)), (arg, client_id))

    con.execute("""
                SELECT * FROM Client
                WHERE id=%s
                """, (client_id, ))
    #con.execute("""
    #                UPDATE client SET name=%s WHERE id=%s;
    #                """, (first_name, client_id))
    conn.commit()
    return

def delete_phone(con, client_id, phone):
    con.execute("""
            DELETE FROM contact WHERE client_id = %s and number = %s;
            """, (client_id, phone))
    conn.commit()
    return

def delete_client(con, client_id):
    con.execute("""
                DELETE FROM contact WHERE client_id = %s;
                """, (client_id, ))
    con.execute("""
                DELETE FROM client WHERE id = %s;
                """, (client_id, ))
    conn.commit()
    return

def find_client(con, first_name=None, last_name=None, email=None, phone=None):
    client_list = {'c.name': first_name, "c.surname": last_name, 'c.email': email, 'Contact.number': phone}
    list_base = {}
    for key, arg in client_list.items():
        if arg != None:
            list_base[key] = arg
    con.execute(f"""
            SELECT c.id, c.name, c.surname, c.email, Contact.number FROM client AS c
            LEFT JOIN Contact ON c.id = Contact.client_id 
            WHERE {[key for key in list_base.keys()][0]}=%s;
            """, ([value for value in list_base.values()][0],))
    print(con.fetchall())
    return

group_client = (
    ['Иван', 'Иванов', 'ivanovich@ya.tam', ['1234']],
    ['Кирил', 'Мамаев', 'kima@yandex.ru', []],
    ['Иван', 'Талов', 'talov@rambler.ru', ['2846652']],
    ['Максим', 'Березовой', '22525@mail.ru', ['7531318', '4454218']],
    ['Мария', 'Макова', 'mama@mail.ru', ['77417']],
    ['Инна', 'Федотова', 'stuard@rambler.ru', ['531684', '4218351', '11443188']]
)

#требуется указать пароль БД
with psycopg2.connect(database="serv_client", user="postgres", password="") as conn:
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE Contact;
            DROP TABLE Client;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS Client(
            id SERIAL PRIMARY KEY,
            name VARCHAR(30) NOT null,
            surname VARCHAR(30) NOT null,
            email VARCHAR(40) NOT null UNIQUE
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Contact(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES client(id),
            number VARCHAR(50) NOT null UNIQUE
        );
        """)
        conn.commit()

        for client in group_client:
            clients = add_client(cur, client[0], client[1], client[2], client[3])

        change = change_client(cur, 2, 'Генадий')
        change = change_client(cur, 6, last_name='Синицина', email='stuard_11@mail.ru')
        del_client = delete_phone(cur, '6', '4218351')
        del_user = delete_client(cur, 4)
        #Согласно условию задачи позволяющая найти клиента по его
        #данным: имени, фамилии, email или телефону, то есть одному параметру
        find = find_client(cur, 'Иван')
        find = find_client(cur, last_name='Макова')

conn.close()