import pytest
import os
from conftest import DummyStore
from remix.db.assets import AssetManager, Image, ImageClass, Asset
import urllib2

def test_image_basics(testimage, settings):
    """upload an image"""
    am = AssetManager(settings.db.testimages, DummyStore(), file_type = Image)
    am.register_file_class(
        ImageClass("title", 
            spec = {'thumb' : dict(width=130),
                    'bigteaser' : dict(width=460, height=460, force=True),
                    'smallteaser' : dict(width=220, height=115, force=True),
                    'small' : dict(width=30, height=30, force=True),
                    'medium' : dict(width=60, height=60, force=True),
                    'title' : dict(width=680, height=300, force=True)
            }
        )
    )

    fp = testimage.open()
    image = am.put(fp, file_class_name="title")
    _id = image._id

    im2 = am[_id]
    assert im2._id == _id
    assert "smallteaser" in im2.data['sizes']
    assert "bigteaser" in im2.data['sizes']

    size = im2['medium']
    assert size.width == 60
    assert size.height == 60
    assert size.url.endswith("medium.png")

    
def test_mp3_basics(testmp3, settings):
    """upload an mp3"""
    am = AssetManager(settings.db.testimages, DummyStore(), file_type = Asset)
    fp = testmp3.open()
    f = am.put(fp)
    _id = f._id

    size = fp.tell()

    mp3 = am[_id]
    assert mp3._id == _id
    fp = open(mp3.url)
    fp.read()
    assert size == fp.tell()

    



    
