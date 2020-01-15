import six
import pytest
from opinionated_configparser import OpinionatedConfigParser


TEST_DICT1 = {
    "section1": {
        "key1": "ééé",
    }
}


def test_python3():
    if six.PY2:
        pytest.skip("python3 test only")
    x = OpinionatedConfigParser()
    x.read_dict(TEST_DICT1)
    assert x.get("section1", "key1") == "ééé"
