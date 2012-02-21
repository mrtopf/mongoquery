from fileexchange.db import FileSet, FileSets, InvalidData, ObjectNotFound
import pytest
import pymongo
import datetime


def test_basics(filesets, fs_data):

    fileset = FileSet(fs_data)
    assert fileset.d.password == "12345"

    fs = filesets.put(fileset)
    fs2 = filesets.get(fs.d._id)
    assert fs2.d.password == "12345"

def test_no_double_init(filesets, fs_data):

    fileset = FileSet(fs_data)
    fs = filesets.put(fileset)

    # get the fs from the db again
    fs = filesets.get(fs.d._id)
    eo1 = fs.d.expires_on # the expires date which should not be set twice
    fs.d.expires_on = datetime.datetime.now() # change it
    fs.save() 

    # get it again
    fs = filesets.get(fs.d._id)
    eo2 = fs.d.expires_on # the expires date which should not be set twice

    assert eo1.timetuple().tm_mday != eo2.timetuple().tm_mday

