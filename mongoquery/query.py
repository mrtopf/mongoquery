import pymongo
import itertools
import functools

__all__ = ['Query', 'Result', 'QueryError']

class QueryError(Exception):
    """a Query Error occurred"""

    def __init__(self, code, msg, query = None):
        """initialize the Query Error.

        :param code: The error code, a lowercase string without spaces
        :param msg: The in depth error description
        :param query: The ``Query`` instance which produced the error
        """

        self.code = code
        self.msg = msg
        self.query = query

    def __repr__(self):
        """return the string representation"""
        return u"""<QueryError code=%s, msg='%s'>""" %(self.code, self.msg)

class Query(object):
    """a MongoDB query object"""

    def __init__(self, **query):
        """initialize the Query object

        :param query: keyword parameters or a dictionary containing the actual query
            to perform. 
        """

        self.query = query
        self._sort = None
        self._limit = None
        self._skip = None
        self.kws = {}
        # a query is meant to be complete as long as not field restrictions
        # are in place
        self._complete = True 
        self._cls = None
        self._coll = None
        self._func = None

    def update(self, **query):
        """add more query elements"""
        self.query.update(query)
        return self

    def sort(self, *args, **kwargs):
        self._sort = (args, kwargs)
        return self

    def limit(self, count):
        self._limit = count
        return self

    def skip(self, count):
        self._skip = count
        return self

    def fields(self, fields):
        self.kws['fields'] = fields
        self._complete = False
        return self

    def cls(self, cls):
        """set the data class to use for every result. This class
        needs to take the resulting document as input"""
        self._cls = cls
        return self

    def coll(self, collection):
        """set the collection to use for the query in front"""
        self._coll = collection
        return self

    def call(self, func, *args, **kwargs):
        """store a function to call for each result item"""
        self._func = (func, args, kwargs)
        return self

    def __call__(self, collection = None):
        """call the Query on a collection and return a ``Result`` instance"""
        if collection is None:
            collection = self._coll
        if collection is None:
            raise QueryError("no_collection", "no collection for the Query was either given in the Query object or via the call", self)
        res = collection.find(self.query, **self.kws)
        if self._sort is not None:
            s = self._sort
            res = res.sort(*s[0], **s[1])
        if self._limit is not None:
            res = res.limit(self._limit)
        if self._skip is not None:
            res = res.skip(self._skip)
        return Result(res, 
                      complete = self._complete,
                      cls = self._cls, 
                      query = self)

class Result(object):
    """a result object"""

    def __init__(self, 
            cursor, 
            complete = True,
            cls = None,
            query = None):
        """initialize the ``Result`` instance with a pymongo cursor instance"""

        self.cursor = cursor
        self.complete = complete
        self.cls = cls
        self.query = query

    def __getitem__(self, a):
        doc = self.cursor[a]
        if self.cls is not None:
            return self.cls(doc)
        return doc

    def __iter__(self, *args, **kwargs):
        iterator = self.cursor.__iter__(*args, **kwargs)

        def instantiate(i):
            return self.cls(i)

        filter_func = None
        # check if we have a class to instantiate. If so then we use
        # the instantiate() function as filter function
        if self.cls is not None:
            filter_func = instantiate
        # if we have a function defined in the query we use that
        elif self.query._func is not None:
            f, args, kwargs = self.query._func
            filter_func = functools.partial(f, *args, **kwargs)
        
        # short cut for no filter function
        if filter_func is None:
            return iterator

        return itertools.imap(filter_func, iterator)

    @property
    def count(self):
        """return the count of matched objects regardless of how many have 
        been returned"""
        return self.cursor.count()

    @property
    def returned(self):
        """return the amount of items returned"""
        return self.cursor.count(True)




