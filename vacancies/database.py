import psycopg2

from prettytable import PrettyTable

class Database():
    # Подключение к БД
    def connect(self):
        try:
            # Подключение к базе данных
            self.connection = psycopg2.connect(
                host='127.0.0.1',
                port=5432,
                user='postgres',
                password='postgres',
                database='vacancy_city',
            )

            print("Успешное подключение к базе данных")

        except Exception as ex:
            print("Ошибка при работе с PostgreSQL:", ex)

    # Удаление таблиц из БД
    def drop_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                DROP TABLE city CASCADE;
                DROP TABLE vacancy CASCADE;
                DROP TABLE vacancycity CASCADE;
                DROP TABLE users CASCADE;
                """)

            # Подтверждение изменений
            self.connection.commit()
            print("Успешно удалены таблицы в БД")

        except Exception as ex:
            print("Ошибка при работе с PostgreSQL:", ex)

    # Создание таблицы БД и связывание таблицы
    def create_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    -- Создание таблицы ГОРОД
                    CREATE TABLE city (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR NOT NULL,
                        foundation_date INT NULL,
                        grp FLOAT NULL,
                        climate VARCHAR NOT NULL,
                        square INT NULL,
                        -- Доступен/недоступен
                        status BOOLEAN NOT NULL,
                        description VARCHAR NOT NULL
                    );

                    -- Создание таблицы ВАКАНСИЯ
                    CREATE TABLE vacancy (
                      id SERIAL PRIMARY KEY,
                      name_vacancy VARCHAR NOT NULL,
                      date_create DATE NOT NULL,
                      date_form DATE NOT NULL,
                      date_close DATE NOT NULL,
                      status_vacancy VARCHAR NOT NULL,
                      id_employer INT NOT NULL,
                      id_moderator INT NOT NULL
                    );

                    -- Создание таблицы ПОЛЬЗОВАТЕЛЬ
                    CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR NOT NULL,
                        password VARCHAR NOT NULL,
                        admin BOOLEAN NOT NULL
                    );

                    -- Создание таблицы ВАКАНСИИГОРОДА
                    CREATE TABLE vacancycity (
                        id SERIAL PRIMARY KEY,
                        id_city INT NOT NULL,
                        id_vacancy INT NOT NULL,
                        quantity_vacancy INT NULL
                    );

                    -- Связывание БД внешними ключами
                    ALTER TABLE vacancycity
                    ADD CONSTRAINT FR_vacancycity_of_city
                        FOREIGN KEY (id_city) REFERENCES city (id);

                    ALTER TABLE vacancycity
                    ADD CONSTRAINT FR_vacancycity_of_vacancy
                        FOREIGN KEY (id_vacancy) REFERENCES vacancy (id);

                    ALTER TABLE vacancy
                    ADD CONSTRAINT FR_vacancy_of_employer
                        FOREIGN KEY (id_employer) REFERENCES users (id);

                    ALTER TABLE vacancy
                    ADD CONSTRAINT FR_vacancy_of_moderator
                        FOREIGN KEY (id_moderator) REFERENCES users (id);
            """)

            # Подтверждение изменений
            self.connection.commit()
            print("Успешно созданы таблицы в БД")

        except Exception as ex:
            print("Ошибка при работе с PostgreSQL:", ex)

    # Заполнение записи в таблицу в БД
    def insert_default_value(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    -- ПОЛЬЗОВАТЕЛЬ (Авторизация)
                    INSERT INTO users (email, password, admin) VALUES
                        ('user1@user.com', '1234', false),
                        ('user2@user.com', '1234', false),
                        ('user3@user.com', '1234', false),
                        ('user4@user.com', '1234', false),
                        ('user5@user.com', '1234', false),
                        ('root@root.com', '1234', true);

                    -- ГОРОД (Услуга)
                    INSERT INTO city (name, foundation_date, grp, climate, square, status, description) VALUES
                        ('Москва', 1147, 13.1, 'умеренный', 2561, true, 'Москва — столица и крупнейший город России. Сюда ведут многие пути и человеческие судьбы, с этим городом связано множество роковых и знаменательных событий истории, людских радостей и надежд, несчастий и разочарований, разумеется, легенд, мифов и преданий. Москва — блистательный город, во всех отношениях достойный называться столицей. Здесь великолепные памятники архитектуры и живописные парки, самые лучшие магазины и высокие небоскребы, длинное метро и заполненные вокзалы. Москва никогда не спит, здесь трудятся с утра до поздней ночи, а затем веселятся до утра.'),
                        ('Санкт-Петербург', 1703, 5.6, 'умеренный', 1439, true, 'Санкт-Петербург – один из красивейших мегаполисов мира, посмотреть на который приезжают путешественники из разных уголков планеты. Раскинувшийся на побережье Финского залива, в устье реки Невы, Санкт-Петербург является вторым по величине городом России (в статусе самостоятельного субъекта федерации) и одновременно административным центром Ленинградской области и Северо-Западного федерального округа.'),
                        ('Екатеринбург', 1723, 1.5, 'умеренный', 495, true, 'Екатеринбург – административный центр Свердловской области, четвёртый по численности город России. Город расположен на Среднем Урале, на восточном склоне Уральских гор. Благодаря тому, что Уральские горы в этом месте представляют собой холмы были проложены дороги из Центральной России в Сибирь. Здесь проходят железные дороги, крупные автодороги, действует международный аэропорт «Кольцово».'),
                        ('Киров', 1374, 1.1, 'умеренный', 169, true, 'Киров – город и областной центр на реке Вятке, известный как родина традиционного народного промысла – дымковской игрушки, вкусного вятского кваса, легкого кукарского кружева и самобытного праздника «Свистопляска». Киров находится в Предуралье, 896 км к северо-востоку от Москвы. Город вошел в историю в роли места ссылок, где издавна отбывали заключение бунтари, не угодные власти. В середине XIX века в вятской ссылке провел семь лет знаменитый русский писатель М. Е. Салтыков-Щедрин.'),
                        ('Волгоград', 1589, 1.3, 'умеренный', 859, true, 'Волгоград - город, один из крупнейших на Юге страны. Его называют портом пяти морей, Волго-Донской канал соединяет теплые южные моря – Черное, Азовское, Каспийское – с холодными Балтийским и Северным. Благодаря этому в городе интенсивно развивается торговля и кипит деловая жизнь. В городе-герое Волгограде находится множество памятников, посвященных героям Великой Отечественной войны.');

                    -- ВАКАНСИЯ (Заявки)
                    INSERT INTO vacancy (name_vacancy, date_create, date_form, date_close, status_vacancy, id_employer, id_moderator) VALUES
                        ('Вакансия №1', '01-01-2023', '10-01-2023', '01-03-2023', 'Введён', 1, 6),
                        ('Вакансия №2', '20-05-2023', '01-06-2023', '01-08-2023', 'В работе', 2, 6),
                        ('Вакансия №3', '24-09-2023', '05-10-2023', '30-11-2023', 'Завершён', 3, 6),
                        ('Вакансия №4', '20-09-2023', '30-09-2023', '30-11-2023', 'Отменен', 4, 6),
                        ('Вакансия №5', '20-09-2023', '30-09-2023', '30-11-2023', 'Удалён', 5, 6);

                    -- ВАКАНСИИГОРОДА (вспомогательная таблица М-М услуга-заявка)
                    INSERT INTO vacancycity (id_city, id_vacancy, quantity_vacancy) VALUES
                        (1, 1, 4),
                        (2, 2, 6),
                        (3, 3, 2),
                        (4, 4, 5),
                        (5, 5, 7);
                    """)

                # Подтверждение изменений
                self.connection.commit()
                print("[vacancycity, city, vacancy, users]: Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[vacancycity, city, vacancy, users]: Ошибка при заполнение данных:", ex)

    # Запрос, который записывает новые данные в таблицу Город
    def insert_city(self, name, foundation_date, grp, climate, square, description):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO city (name, foundation_date, grp, climate, square, description) VALUES
                            (%s, %s, %s, %s, %s, %s);""",
                    (name, foundation_date, grp, climate, square, description)
                )

                # Подтверждение изменений
                self.connection.commit()
                print("[city] Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[city] Ошибка при заполнение данных:", ex)

    # Запрос, который записывает новые данные в таблицу Вакансия
    def insert_vacancy(self, name_vacancy, date_create, date_publication, date_close, status_vacancy, id_employer,
                       id_moderator):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO vacancy (name_vacancy, date_create, date_publication, date_close, status_vacancy, id_employer, id_moderator) VALUES
                             (%s, %s, %s, %s, %s, %s, %s);""",
                    (name_vacancy, date_create, date_publication, date_close, status_vacancy, id_employer, id_moderator)
                )

                # Подтверждение изменений
                self.connection.commit()
                print("[vacancy] Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[vacancy] Ошибка при заполнение данных:", ex)

    # Запрос, который записывает новые данные в таблицу ВакансииГорода
    def insert_vacancycity(self, id_city, id_vacancy):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO vacancycity (id_city, id_vacancy) VALUES
                               (%s, %s);""",
                    (id_city, id_vacancy)
                )

                # Подтверждение изменений
                self.connection.commit()
                print("[vacancycity] Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[vacancycity] Ошибка при заполнение данных:", ex)

    # Выводит все записи
    def select_all(self):
        try:
            with self.connection.cursor() as cursor:
                database = {}
                name_table = ['users', 'city', 'vacancy', 'vacancycity']
                database['name_table'] = name_table
                for name in name_table:
                    cursor.execute(f"""SELECT * FROM {name};""")
                    database[name] = cursor.fetchall()
                    # Получим названия колонок из cursor.description
                    database[f'{name}_name_col'] = [col[0] for col in cursor.description]

                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("Ошибка при чтении данных:", ex)

    # Печать для вывода все записи
    def print_select_all(self, database):
        data_print = []

        for name in database['name_table']:
            table = PrettyTable()
            table.field_names = database[f'{name}_name_col']
            for row in database[name]:
                table.add_row(row)
            # Выводим таблицу на консоль
            # print(table)
            data_print.append(table)

        return data_print

    # Обновление статуса в таблице Город
    def update_status_delete_city(self, status, id_city):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE city SET status = %s WHERE id = %s;""",
                    (status, id_city)
                )
                # Подтверждение изменений
                self.connection.commit()
                print("[Status] Данные успешно обновлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[Status] Ошибка при обновление данных:", ex)

    # Выводит записи в таблицу Город в котором статус доступен
    def get_city_with_status_true(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM city as C
                        WHERE C.status = true;
                    """)
                # Получаем данные
                results = cursor.fetchall()
                # Подтверждение изменений
                self.connection.commit()
                print("[City] Данные успешно прочитаны")

                database = []
                for obj in results:
                    data = {
                        'id': obj[0],
                        'name': obj[1],
                        'foundation_date': obj[2],
                        'grp': obj[3],
                        'climate': obj[4],
                        'square': obj[5],
                        'status': obj[6],
                        'description': obj[7],
                    }
                    database.append(data)

                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[City] Ошибка при чтение данных:", ex)

    # Выводит записи таблицы Город
    def get_city_for_id(self, id_city):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """SELECT * FROM city as C
                        WHERE C.id = %s;
                    """, (id_city,)
                )
                # Получаем данные
                results = cursor.fetchall()
                # Подтверждение изменений
                self.connection.commit()
                print("[Vacancy_City] Данные успешно прочитаны")

                database = []
                for obj in results:
                    data = {
                        'id': obj[0],
                        'name': obj[1],
                        'foundation_date': obj[2],
                        'grp': obj[3],
                        'climate': obj[4],
                        'square': obj[5],
                        'status': obj[6],
                        'description': obj[7],
                    }
                    database.append(data)

                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[Vacancy_City] Ошибка при чтение данных:", ex)

    def get_vacancycity_by_id(self, id_city):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """SELECT
                            VC.id,
                            C.name,
                            C.climate,
                            C.square,
                            C.status,
                            V.name_vacancy,
                            V.status_vacancy
                        FROM vacancycity as VC
                        INNER JOIN city as C ON VC.id_city = C.id
                        INNER JOIN vacancy as V ON VC.id_vacancy = V.id
                        WHERE C.id = %s;
                    """, (id_city,)
                )
                # Получаем данные
                results = cursor.fetchall()
                # Подтверждение изменений
                self.connection.commit()
                print("[Vacancy_City] Данные успешно прочитаны")

                database = []
                for obj in results:
                    data = {
                        'vc_id': obj[0],
                        'c_name': obj[1],
                        'c_climate': obj[2],
                        'c_square': obj[3],
                        'c_status': obj[4],
                        'v_name_vacancy': obj[5],
                        'v_status_vacancy': obj[6],
                    }
                    database.append(data)

                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[Vacancy_City] Ошибка при чтение данных:", ex)

    # Закрытие БД
    def close(self):
        # Закрытие соединения
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")


# Вызов функции
db = Database()
# Вызов функции для подключения к БД
db.connect()

# Вызов функции для удаления таблицы в БД
# db.drop_table()

# Вызов функции для создания таблицы в БД
# db.create_table()

# Вызов функции для заполнения записей в таблицу БД
# db.insert_default_value()

# Вызов функции для добавления новых записей города
# # db.insert_city()
# Вызов функции для добавления новых записей вакансий
# # db.insert_vacancy()
# Вызов функции для добавления новых записей вакансиигорода
# # db.insert_vacancycity()

# Вызов функции для вывода все записи
# # db.select_all()
# Вызов функции печать для вывода все записи
# # db.print_select_all()

# Вызов функции для обновления статуса в таблице Город
# db.update_status_delete_city(True, 5)

# Вызов функции для вывода записей из разных таблиц в одну таблицу
# db.get_vacancycity()
# db.get_vacancycity_by_id(1)

# Вызов функции для вывода записи в таблицу Город в котором статус доступен
# db.get_city_with_status_true()

# Вызов функции для закрытия БД
db.close()