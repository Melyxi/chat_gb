import hmac
import sqlite3
import re

SECRET_KEY = b'HeiwrjJFEI54964fdsaKKFefkwpe'


class UserModel:
    def __init__(self, url_base):
        self.url_base = url_base
        self.namemodel = self.__class__.__name__
        self.id = 'id  INTEGER primary key'
        self.username = 'username varchar(30) not NULL UNIQUE'
        self.password = '`password` varchar(40) not null'
        self.is_active = 'is_active TINYINT default 0'

        attr = []
        for name, value in vars(self).items():
            if not value == self.url_base:
                if not value == self.namemodel:
                    attr.append(value)
        self.str_atr = ', '.join(attr)

    def migrate(self):
        with sqlite3.connect(self.url_base) as conn:
            print(f"create table if not exists {self.namemodel} ({self.str_atr});")
            cursor = conn.cursor()
            cursor.execute(
                f"create table if not exists {self.namemodel} ({self.str_atr});")


class HistoryClient:
    def __init__(self, url_base):
        self.url_base = url_base
        self.namemodel = self.__class__.__name__
        self.id_history = 'id INTEGER primary key'
        self.username_id = 'username_id INT'
        self.time_at = 'time_at DATETIME'
        self.ip_addr = 'ip_addr varchar(40) not null'
        self.foreign_key = 'FOREIGN KEY (username_id) REFERENCES UserModel(id) ON UPDATE CASCADE ON DELETE CASCADE'

        attr = []
        for name, value in vars(self).items():
            if not value == self.url_base:
                if not value == self.namemodel:
                    attr.append(value)
        self.str_atr = ', '.join(attr)

    def migrate(self):
        with sqlite3.connect(self.url_base) as conn:
            cursor = conn.cursor()
            print(f"create table if not exists {self.namemodel} ({self.str_atr});")
            cursor.execute(
                f"create table if not exists {self.namemodel} ({self.str_atr});")


class ListClients:
    def __init__(self, url_base):
        self.url_base = url_base
        self.namemodel = self.__class__.__name__
        self.id_history = 'id INTEGER primary key'
        self.username_id = 'username_id INT'
        self.client_id = 'client_id INT'
        self.foreign_key1 = 'FOREIGN KEY (username_id) REFERENCES UserModel(id) ON UPDATE CASCADE ON DELETE CASCADE'
        self.foreign_key = 'FOREIGN KEY (client_id) REFERENCES UserModel(id) ON UPDATE CASCADE ON DELETE CASCADE'

        attr = []
        for name, value in vars(self).items():
            if not value == self.url_base:
                if not value == self.namemodel:
                    attr.append(value)
        self.str_atr = ', '.join(attr)

    def migrate(self):
        with sqlite3.connect(self.url_base) as conn:
            cursor = conn.cursor()
            print(f"create table if not exists {self.namemodel} ({self.str_atr});")
            cursor.execute(
                f"create table if not exists {self.namemodel} ({self.str_atr});")


class ObjRelMap:
    def __init__(self, url_base):
        self.url_base = url_base
        self.conn = None
        self.cursor = None

    def initialization(self):
        conn = sqlite3.connect(self.url_base)
        cursor = conn.cursor()
        self.conn = conn
        self.cursor = cursor

    def add(self, model, parameter):
        self.initialization()
        keys = []
        values = []
        str_k = '('
        for key, value in parameter.items():
            str_k += '?,'
            keys.append(key)
            values.append(value)
        str_k = str_k[:-1]
        str_k += ')'
        keys = tuple(keys)
        values = tuple(values)
        try:
            self.cursor.execute(f"INSERT INTO {model}{keys} values {str_k}", values)
        except BaseException as e:
            print('Error: add', e)
        self.conn.commit()
        self.conn.close()

    def select(self, model, parameters):
        self.initialization()
        str_join = ', '.join(parameters)
        try:
            self.cursor.execute(f"SELECT {str_join} FROM {model} ")
            results = self.cursor.fetchall()
            return results
        except BaseException as e:
            print('Error: select', e)
        self.conn.close()

    def get(self, model, parameters, field):
        self.initialization()
        # print(f"SELECT {parameters} FROM {model} ")
        str_join = ', '.join(parameters)
        keys = []
        values = []

        list_filter = []

        for key, value in parameters.items():
            str_filter = key + '=:' + key
            list_filter.append(str_filter)
            keys.append(key)
            values.append(value)

        filter_join = ' and '.join(list_filter)

        key_join = ', '.join(field)

        try:

            self.cursor.execute(f"SELECT {key_join} FROM {model} WHERE {filter_join}", parameters)
            results = self.cursor.fetchall()

            return results[0]
        except BaseException as e:
            print('Error: get', e)
        self.conn.close()

    def update(self, model, where, parameters):
        self.initialization()

        filter_update = []
        filter_where = []
        for key, value in where.items():
            str_filter = key + '=:' + key
            filter_where.append(str_filter)

        for key, value in parameters.items():
            str_filter = key + '=:' + key
            filter_update.append(str_filter)
            where[key] = value

        filter_where = ' and '.join(filter_where)
        filter_update = ' and '.join(filter_update)

        try:
            self.cursor.execute(f"UPDATE {model} SET {filter_update} WHERE {filter_where}", where)
            self.conn.commit()

        except BaseException as e:
            print('Error: update', e)
        self.conn.close()

    def delete(self, model, where):
        self.initialization()

        filter_where = []
        for key, value in where.items():
            str_filter = key + '=:' + key
            filter_where.append(str_filter)

        filter_where = ' and '.join(filter_where)

        try:
            self.cursor.execute(f"DELETE FROM {model} WHERE {filter_where}", where)
            self.conn.commit()
        except BaseException as e:
            print('Error: delete', e)

    def join(self, models, field=None, where=None):
        self.initialization()

        for obj in models:

            string = getattr(obj, 'foreign_key', False)
            print(string)
            if string:

                pattern = r'\((.+?)\)'
                pattern1 = r'\(([a-z]+)\)'
                key_id = re.search(pattern, string)
                key_ref = re.search(pattern1, string)

                key_id = key_id.group(1)
                key_ref = key_ref.group(1)
                print(key_id)
                print(key_ref)
                model_key = obj.namemodel
            else:
                model_ref = obj.namemodel
                print(model_ref)

        if field != None:
            key_join = ', '.join(field)
        else:
            key_join = '*'

        if where != None:
            where = f'WHERE {where}'
        else:
            where = ''

        try:

            self.cursor.execute(
                f"SELECT {key_join} FROM {model_ref} INNER JOIN {model_key} ON {model_ref}.{key_ref}={model_key}.{key_id} {where}")

            results = self.cursor.fetchall()

            return results
        except BaseException as e:
            print('Error: join', e)
        self.conn.close()


def register_user(password):
    hash = hmac.new(SECRET_KEY, bytes(password, encoding='utf-8'), digestmod='sha256')
    digest = hash.hexdigest()
    return digest

if __name__ == '__main__':
    user = UserModel('company.db3')
    user.migrate()
    history = HistoryClient('company.db3')
    history.migrate()
    list_clients = ListClients('company.db3')
    list_clients.migrate()

    # name = 'igor'
    # password = '123'
    #

    cliendb = ObjRelMap('company.db3')

    password = '12345'
    pass_hash = register_user(password)

    list_data = {'username': 'igor2', 'password': pass_hash}

    cliendb.add('UserModel', list_data)

    # cliendb.select('UserModel', ['id', 'username', 'password'])
    #
    dict_get = {'username': 'igor2'}
    #
    field = ['id', 'password']
    #
    get = cliendb.get('UserModel', dict_get, field)
    print(get, 'get_user')
    #
    # update_set = {'is_active': 1}
    # cliendb.update('UserModel', dict_get, update_set)
    #
    # history_add = {'username_id': 1, 'time_at': '2015-02-25 13:21:49', 'ip_addr': '127.0.0.1'}
    #
    # f = cliendb.select('UserModel', ['id', 'username', 'password'])
    #
    # cliendb.join([user, history], field=['UserModel.username'], where='UserModel.id=1')
    #
    # join_db = cliendb.join([user, list_clients], field=['UserModel.username'], where='ListClients.username_id=1')
    #
    # db_user_add = cliendb.get('UserModel', {'username': 'igor'}, ['id'])
    # user_add = cliendb.get('UserModel', {'username': 'egor'}, ['id'])
    #
    # print(db_user_add)
    # print(user_add)
    #
    # print(join_db)
    # for item in join_db:
    #     print(item[0])
    #
    # cliendb.delete('ListClients', {"username_id": 1, "client_id": 3})
    #
    # join_db = cliendb.join([user, list_clients], field=['UserModel.username'],
    #                        where=f'ListClients.username_id=2')
    # print(join_db)
