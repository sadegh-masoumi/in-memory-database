"""
main model
version 1.0.0
date 2022
"""

import json
from pathlib import Path

from database import DatabaseModel


class InterFace:
    """ InterFace"""

    def __init__(self):
        """ Initialize Default database"""
        self.database = DatabaseModel()
        self.list_of_db = [self.database]

    @staticmethod
    def clean_terminal():
        print(chr(27) + "[2J")

    def _set(self) -> None:
        command = input().split()
        if command[0] != 'set' or len(command) != 3:
            print("Invalid command")
            return
        try:
            self.database.set_data(key=command[1], value=json.loads(command[2]))
        except json.decoder.JSONDecodeError:
            print('your value is not valid')
            return

        print('>')

    def _get(self) -> None:
        command = input().split()
        if command[0] != 'get' or len(command) != 2:
            print("Invalid command!")
            return
        try:
            value = self.database.get_data(command[1])
        except KeyError:
            print('This key does not exist in the database')
            return
        print('> ' + str(value))

    def _del(self) -> None:
        command = input().split()
        if command[0] != 'del' or len(command) != 2:
            print("Invalid command!")
            return
        try:
            self.database.delete(command[1])
        except KeyError:
            print('This key does not exist in the database')
            return
        print('>')

    def _get_by_regex(self):
        command = input().split()
        if command[0] != 'keys' or len(command) != 2:
            print("Invalid command")
            return
        print('> ' + str(self.database.get_keys_by_regex(command[1])))

    def _show_list_of_db(self):
        command = input().split()
        if command[0] != 'list' or len(command) != 1:
            print("Invalid command!")
            return

        print('> ' + str(self.list_of_db))

    def _change_db(self):
        command = input().split()
        if command[0] != 'use' or len(command) != 2:
            print("Invalid command")
            return

        for db in self.list_of_db:
            if str(db) == command[1]:
                self.database = db
                break
        else:
            self.database = DatabaseModel(name=command[1])
            self.list_of_db.append(self.database)

        print('>')

    def _load_db(self):
        command = input().split()
        if command[0] != 'load' or len(command) != 3:
            print("Invalid command")
            return

        filepath = Path(command[1] + '.json')

        self._create_db(command[2])
        database = self._get_db_by_name(command[2])

        with open(filepath, 'r') as f:
            database.db = json.load(f)

        print('>')

    def _get_db_by_name(self, name):
        for db in self.list_of_db:
            if str(db) == name:
                return db
        raise Exception('this db is not exit')

    def _create_db(self, name):
        """create database
        :return True if create database
        :return false if name is duplicate
        """
        for db in self.list_of_db:
            if str(db) == name:
                return False
        self.database = DatabaseModel(name)
        self.list_of_db.append(self.database)
        return True

    def _dump_db(self):
        command = input().split()
        if command[0] != 'dump' or len(command) != 3:
            print("Invalid command")
            return

        for db in self.list_of_db:
            if str(db) == command[1]:
                db.dump(command[2])
                break
        else:
            print('There is no database with this name')
            return
        print('>')

    @staticmethod
    def _print(*args):
        print('>', *args)

    def main(self):
        print('Welcome to in memory database')
        print('database in use : ' + str(self.database))
        while True:
            action = input().split()

            if action[0] != '#':
                print("Invalid command! your command must be start with #")

            elif action == ['#', 'set', 'key', 'value']:
                self._set()

            elif action == ['#', 'get', 'key']:
                self._get()

            elif action == ['#', 'del', 'key']:
                self._del()

            elif action == ['#', 'keys', 'regex']:
                self._get_by_regex()

            elif action == ['#', 'use', 'db_name']:
                self._change_db()

            elif action == ['#', 'list']:
                self._show_list_of_db()

            elif action == ['#', 'dump', 'db_name', 'path']:
                self._dump_db()

            elif action == ['#', 'load', 'path', 'db_name']:
                self._load_db()

            elif action == ['#', 'exit']:
                break

            else:
                print('Invalid command!')


if __name__ == "__main__":
    interface = InterFace()
    interface.main()
