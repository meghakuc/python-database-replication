#!/usr/bin/env python

import getopt
import sys
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

def make_session(connection_string):
    engine = create_engine(connection_string, echo=False, convert_unicode=True)
    Session = sessionmaker(bind=engine, autoflush=False)
    return Session(), engine

def create_table(from_db, to_db):
    source, sengine = make_session(from_db)
    smeta = MetaData(bind=sengine)
    destination, dengine = make_session(to_db)
    tables = sengine.table_names()

    for table_name in tables:
        print ('Processing', table_name)
        if (table_name == "sqlite_sequence") or (table_name == "sqlite_stat1"):
            print('Skipping!!')
            continue
        print ('Pulling schema from source server')
        table = Table(table_name, smeta, autoload=True)
        print ('Creating table on destination server')
        table.metadata.create_all(dengine)

    print ('Committing changes')
    destination.commit()

def print_usage():
    print ("""
Usage: %s -f source_server -t destination_server
    -f, -t = driver://user[:password]@host[:port]/database

Example: %s -f oracle://someuser:PaSsWd@db1/TSH1 \\
    -t mysql://root@db2:3307/reporting
    """ % (sys.argv[0], sys.argv[0]))

if __name__ == '__main__':
    optlist, tables = getopt.getopt(sys.argv[1:], 'f:t:')

    options = dict(optlist)
    if '-f' not in options or '-t' not in options:
        print_usage()
        raise SystemExit(1)

    create_table(
        options['-f'],
        options['-t']
    )
