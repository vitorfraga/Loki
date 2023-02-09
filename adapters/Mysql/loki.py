# python3 loki.py --server localhost --port 3306 --user loki --password loki  --database loki_database --table users --insert 100 --update 100 --delete

from faker import Faker
import argparse
import faker
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import pymysql
from sqlalchemy.engine.result import ResultMetaData
from sqlalchemy.sql.expression import insert, select, func
import time


class dataFake:
    def __init__(self, mysql_settings, database, table, insert, update, delete, sleep):

        self._server = mysql_settings['server']
        self._port = mysql_settings['port']
        self._user = mysql_settings['user']
        self._password = mysql_settings['password']
        self._database = database
        self._table = table
        self._insert = insert
        self._update = update
        self._delete = delete
        self._sleep = sleep
        self._fake = Faker()

        pass

    def insert(self):

        engine = create_engine('Mysql+pymysql://'+self._user+':'+self._password+'@'+self._server+':'+self._port+'/'+self._database)
        meta = MetaData()
        table = Table(
        self._table, meta,
        Column('id', Integer, primary_key = True),
        Column('name', String(255)))


        for _ in range(self._insert):

            ins = table.insert().values(name =self._fake.name())
            conn = engine.connect()
            result = conn.execute(ins)
            print("INSERT:"+str(result.lastrowid) + ','+self._fake.name())
            # time.sleep(self._sleep)


    def update(self):

        meta = MetaData()
        table = Table(
        self._table, meta,
        Column('id', Integer, primary_key = True),
        Column('name', String(255)))

        engine = create_engine('Mysql+pymysql://' + self._user + ':' + self._password + '@' + self._server + ':' + self._port + '/' + self._database)
        query = select([table]).order_by(func.rand()).limit(self._update)
        result = engine.execute(query)
        for row in result:
            id = row[0]
            old_name = row[1]
            new_name = self._fake.name()
            action = table.update().values(name = new_name).where(table.c.id == id)
            conn = engine.connect()
            result = conn.execute(action)
            print("UPDATED: "+str(id))
    def delete(self):

        meta = MetaData()
        table = Table(
        self._table, meta,
        Column('id', Integer, primary_key = True),
        Column('name', String(255)))

        engine = create_engine('Mysql+pymysql://' + self._user + ':' + self._password + '@' + self._server + ':' + self._port + '/' + self._database)
        query = select([table]).order_by(func.rand()).limit(self._delete)
        result = engine.execute(query)
        for row in result:
            id = row[0]
            action = table.delete().where(table.c.id == id)
            conn = engine.connect()
            result = conn.execute(action)
            print("DELETED: "+str(id))

    def create_datebase(self):

        engine = create_engine('Mysql+pymysql://root:password@127.0.0.1:3308', pool_recycle=3600, pool_size=10, max_overflow=20)
        engine = create_engine(
            'Mysql+pymysql://' + self._user + ':' + self._password + '@' + self._server + ':' + self._port,pool_recycle=3600, pool_size=10, max_overflow=20)
        engine.execute("CREATE DATABASE IF NOT EXISTS "+self._database)
        print("CREATE DATABASE: "+self._database)


    def create_table(self):

        engine = create_engine('Mysql+pymysql://' + self._user + ':' + self._password + '@' + self._server + ':' + self._port + '/' + self._database)
        meta = MetaData()
        table = Table(
        self._table, meta,
        Column('id', Integer, primary_key = True),
        Column('name', String(255))

        )
        meta.create_all(engine)
        print("CREATE TABLE: "+self._table)


    def db_random(iterations):
        pass


def main():
    if __name__ == '__main__':

        app_parser = argparse.ArgumentParser(allow_abbrev=False)


        app_parser.add_argument('--server',
                                action='store',
                                type=str,
                                required=False,
                                dest='server',
                                help='Server name')

        app_parser.add_argument('--port',
                                action='store',
                                type=str,
                                required=False,
                                dest='port',
                                help='Port number')

        app_parser.add_argument('--user',
                                action='store',
                                type=str,
                                required=False,
                                dest='user',
                                help='User name')

        app_parser.add_argument('--password',
                                action='store',
                                type=str,
                                required=False,
                                dest='password',
                                help='Password value')


        app_parser.add_argument('--database',
                                action='store',
                                type=str,
                                required=False,
                                dest='database',
                                help='Database name')

        app_parser.add_argument('--table',
                                action='store',
                                type=str,
                                required=False,
                                dest='table',
                                help='Table name')

        app_parser.add_argument('--insert',
                                action='store',
                                type=int,
                                required=False,
                                dest='insert',
                                default=0,
                                help='Total insert rows')

        app_parser.add_argument('--update',
                                action='store',
                                type=int,
                                required=False,
                                dest='update',
                                default=0,
                                help='Total update rows')

        app_parser.add_argument('--delete',
                                action='store',
                                type=int,
                                required=False,
                                dest='delete',
                                default=0,
                                help='Total delete rows')

        app_parser.add_argument('--sleep',
                                action='store',
                                type=float,
                                required=False,
                                dest='sleep',
                                default=0.3,
                                help='Sleep time')


        file = open('../../logo.txt', "r")
        print(file.read())

        args = app_parser.parse_args()
        mysql_settings = {'server': args.server, 'port': args.port, 'user': args.user, 'password': args.password}

        dummy = dataFake(mysql_settings, args.database, args.table, args.insert, args.update, args.delete, args.sleep)

        dummy.create_datebase()
        dummy.create_table()
        dummy.insert()
        dummy.update()
        dummy.delete()


if __name__ == "__main__":
    main()








