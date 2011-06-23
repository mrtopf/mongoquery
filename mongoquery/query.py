import pymongo
import itertools

__all__ = ['Query', 'Result']


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

    def __call__(self, collection):
        """call the Query on a collection and return a ``Result`` instance"""
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
        if self.cls is None:
            return iterator

        def instantiate(i):
            return self.cls(i)

        return itertools.imap(instantiate, iterator)

    @property
    def count(self):
        """return the count of matched objects regardless of how many have 
        been returned"""
        return self.cursor.count()

    @property
    def returned(self):
        """return the amount of items returned"""
        return self.cursor.count(True)




