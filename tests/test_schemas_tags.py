import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.schemas.tags import Tagscreate, Tagsupdate, TagsResponse

def test_tagscreate_schema():
    data = {"name": "Science", "description": "Science générale"}
    tag = Tagscreate(**data)
    assert tag.name == "Science"
    assert tag.description == "Science générale"

def test_tagsupdate_schema():
    data = {"name": None, "description": "Mise à jour"}
    tag = Tagsupdate(**data)
    assert tag.name is None
    assert tag.description == "Mise à jour"

def test_tagsresponse_schema():
    data = {"id": 1, "name": "Roman", "description": None}
    tag = TagsResponse(**data)
    assert tag.id == 1
    assert tag.name == "Roman"
    assert tag.description is None
