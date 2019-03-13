#!/usr/bin/env python

import getopt
import sys
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def make_session(connection_string):
    engine = create_engine(connection_string, echo=False, convert_unicode=True)
    Session = sessionmaker(bind=engine, autoflush=False)
    return Session(), engine
    
def data_transfer(from_db, to_db):
    source, sengine = make_session(from_db)
    destination, dengine = make_session(to_db)
    smeta = MetaData()
    smeta.reflect(bind=sengine)
    for table in smeta.sorted_tables:
        table_name = table.name
        print ('Processing', table_name)
        if (table_name == "sqlite_sequence") or (table_name == "sqlite_stat1"):
            print('Skipping!!')
            continue
        NewRecord = quick_mapper(table)
        columns = table.columns.keys()
        print ('Transferring records')
        for record in source.query(table).all():
            data = dict(
                [(str(column), getattr(record, column)) for column in columns]
            )
            destination.merge(NewRecord(**data))
        print ('Committing changes for table: ',table_name)
        destination.commit()

def print_usage():
    print ("""
Usage: %s -f source_server -t destination_server
    -f, -t = driver://user[:password]@host[:port]/database

Example: %s -f oracle://someuser:PaSsWd@db1/TSH1 \\
    -t mysql://root@db2:3307/reporting
    """ % (sys.argv[0], sys.argv[0]))

def quick_mapper(table):
    Base = declarative_base()
    class GenericMapper(Base):
        __table__ = table
    return GenericMapper

if __name__ == '__main__':
    optlist, tables = getopt.getopt(sys.argv[1:], 'f:t:')

    options = dict(optlist)
    if '-f' not in options or '-t' not in options:
        print_usage()
        raise SystemExit(1)

    data_transfer(
        options['-f'],
        options['-t']
    )
