import pymongo

def pytest_funcarg__db(request):
    db = pymongo.Connection().mongoquery_tests
    db.test.drop()

    # add some documents
    docs = [ 
        {'a' : 1, 
         'b' : 2,
         'c' : 1,
        },
        {'a' : 2, 
         'b' : 3,
         'c' : 1,
        }
    ]
    db.test.insert(docs)
    return db

def pytest_funcarg__cls(request):

    class Record(dict):
        pass

        @property
        def g(self):
            return self['a'] + self['b']

    return Record
