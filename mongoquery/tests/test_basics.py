from mongoquery import Query, QueryError
import pytest

def test_basics(db):
    q = Query(a=2)
    r = q(db.test)
    assert r[0]['b'] == 3
    assert r.complete

def test_count(db):
    q = Query(c=1)
    assert q(db.test).count  == 2

def test_iter(db):
    q = Query(c=1)
    r = set()
    for i in q(db.test):
        r.add(i['a'])
    assert r == set([1,2])

def test_sort(db):
    q = Query(c=1).sort("a")
    assert q(db.test)[0]['a'] == 1
    assert q(db.test)[1]['a'] == 2

    q = Query(c=1).sort("a", -1)
    assert q(db.test)[0]['a'] == 2
    assert q(db.test)[1]['a'] == 1

def test_limit(db):
    q = Query(c=1).sort("a").limit(1)
    assert q(db.test).returned == 1
    q = Query(c=1).sort("a").limit(2)
    assert q(db.test).returned == 2

def test_skip(db):
    q = Query(c=1).sort("a").limit(2).skip(1)
    assert q(db.test).returned == 1
    assert q(db.test)[0]['a']==2

    q = Query(c=1).sort("a").limit(2).skip(0)
    assert q(db.test).returned == 2
    assert q(db.test)[0]['a']==1

def test_fields(db):
    q = Query(c=1).sort("a").fields('b')
    r = q(db.test)
    assert set(r[0].keys()) == set(["b","_id"])
    assert not r.complete

def test_cls(db, cls):
    q = Query(c=1).sort("a").limit(1).cls(cls)
    r = q(db.test)
    assert isinstance(r[0], cls)
    assert r[0].g == 3

def test_cls_iter(db, cls):
    q = Query(c=1).sort("a").limit(1).cls(cls)
    r = q(db.test)
    for item in r:
        assert item.g == 3

def test_set_collection(db, cls):
    q = Query(a=2).coll(db.test)
    r = q()
    assert r[0]['b'] == 3
    assert r.complete

def test_no_set_collection(db, cls):
    q = Query(a=2)
    pytest.raises(QueryError, q)
    try:
        r = q()
    except QueryError, e:
        assert e.code == "no_collection"

