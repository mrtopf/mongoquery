from fileexchange.db import FileSet, FileSets
import pymongo
import datetime

def pytest_funcarg__db(request):
    """return a database object"""
    conn = pymongo.Connection()
    db = conn.fileset_testdatabase
    return db

def pytest_funcarg__filesets(request):
    """return a database object"""
    db = request.getfuncargvalue("db")
    db.filesets.remove()
    return FileSets(db.filesets)

def pytest_funcarg__fs_data(request):
    """return dummy data for a fileset"""
    return {
        'oid' : "c76s87c68c7s6",
        'password' : '12345',
        'subject' : "Subject 1",
        'description' : "This is a description",
        'sender_id' : None,
        'sender_email' : "foo@example.org",
        'sender_name' : "Example sender",
        'recipient_id' : "info@kua-nrw.de",
        'from_kua' : False,
        'expires_on' : datetime.datetime.now(),
        'created_ip' : "127.0.0.1",
        'size' : 1761716176,
    }

