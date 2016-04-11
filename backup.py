#! /usr/bin/env python2

import sqlite3
import argparse
import datetime
import shutil


# todo: add encryption support with subprocess and gpg


argprs = argparse.ArgumentParser(description='backup database')
argprs.add_argument(
    '--storage-service',
    dest='strsrv',
    help='e.g. google-drive'
)
argprs.add_argument(
    '--database',
    dest='db',
    help='database file path'
)
args = argprs.parse_args()

db = sqlite3.connect(args.db)
db.execute('begin immediate')

bkp_db = '{0}.{1}.bkp'.format(args.db, datetime.datetime.utcnow().strftime('%Y-%m-%d.%H-%M-%S.%f'))
# todo: upload backup file to google drive
shutil.copyfile(args.db, bkp_db)

db.rollback()
