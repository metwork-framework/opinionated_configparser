import os
import pytest
from opinionated_configparser import render_string
from opinionated_configparser import OpinionatedConfigParser


TEST_DICT1 = {
    "section1": {
        "key1": "value1{{ENV_VAR}}",
    }
}


def test_envtpl():
    if "ENV_VAR" in os.environ:
        del os.environ["ENV_VAR"]
    x = OpinionatedConfigParser(use_envtpl=True)
    x.read_dict(TEST_DICT1)
    try:
        render_string("foo")
    except Exception:
        pytest.skip("envtpl support missing => skipping")
    assert x.get("section1", "key1") == "value1"


def test_envtpl2():
    os.environ["ENV_VAR"] = "foo"
    x = OpinionatedConfigParser(use_envtpl=True)
    x.read_dict(TEST_DICT1)
    try:
        render_string("foo")
    except Exception:
        pytest.skip("envtpl support missing => skipping")
    assert x.get("section1", "key1") == "value1foo"
    del os.environ["ENV_VAR"]
