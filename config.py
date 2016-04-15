#! /usr/bin/env python2

from argon2 import PasswordHasher
import getpass
import os
import sqlite3
import sys


def make_secret_key():
    with open('secret_key', 'w') as secret_key_file:
        secret_key_file.write('{0}\n'.format(os.urandom(48)))


def read_secret_key():
    try:
        with open('secret_key', 'r') as secret_key_file:
            return secret_key_file.read()
    except IOError:
        pass


def make_passwd():
    username = raw_input('Username: ')
    password = getpass.getpass()
    password_verfiy = getpass.getpass('Verify Password:')
    if password != password_verfiy:
        print('Passwords differed, aborting')
    with open('passwd', 'w') as passwd_file:
        passwd_file.write(
            '{0}:{1}\n'.format(username, PasswordHasher().hash(password))
        )


def read_passwd():
    try:
        with open('passwd', 'r') as passwd_file:
            return dict(
                line.strip().split(':', 1) for line in passwd_file.readlines()
            )
    except IOError:
        pass


def init_database():
    if Config.DATABASE_TYPE == 'sqlite':
        with open('schema_sqlite.sql', 'r') as schema:
            database = sqlite3.connect(Config().DATABASE)
            database.cursor().executescript(schema.read())
            database.commit()
            database.close()


class Config(object):
    DATABASE_TYPE = 'sqlite'
    DATABASE = 'webdmp.db'
    SECRET_KEY = read_secret_key()
    PASSWD = read_passwd()


class DevelConfig(Config):
    DEBUG = True


if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            if sys.argv[1] == 'init':
                make_secret_key()
                make_passwd()
                try:
                    os.remove('webdmp.db')
                except:
                    pass
                init_database()
            elif sys.argv[1] == 'secret_key':
                make_secret_key()
            elif sys.argv[1] == 'passwd':
                make_passwd()
            else:
                raise NameError()
        else:
            raise NameError()
    except NameError:
        print('Usage: %s {init|secret_key|passwd}' % sys.argv[0])
