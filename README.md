# opinionated_configparser

[//]: # (automatically generated from https://github.com/metwork-framework/resources/blob/master/cookiecutter/_%7B%7Bcookiecutter.repo%7D%7D/README.md)

**Status (master branch)**



[![Drone CI](http://metwork-framework.org:8000/api/badges/metwork-framework/opinionated_configparser/status.svg)](http://metwork-framework.org:8000/metwork-framework/opinionated_configparser)
[![Maintenance](https://github.com/metwork-framework/resources/blob/master/badges/maintained.svg)]()
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/metwork-framework/opinionated_configparser/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/metwork-framework/opinionated_configparser/?branch=master)
[![codecov](https://codecov.io/gh/metwork-framework/opinionated_configparser/branch/master/graph/badge.svg)](https://codecov.io/gh/metwork-framework/opinionated_configparser)


[//]: # (TABLE_OF_CONTENTS_PLACEHOLDER)

## What is it?

This is an opinionated Python3 thin layer over the [Python configparser library](https://docs.python.org/3/library/configparser.html) to deal with:

- configuration variants (PROD, DEV...) expressed as alternative keys in ini file
- (optional) [envtpl](https://github.com/metwork-framework/envtpl) support within configuration values (so you can use [Jinja2](https://jinja.palletsprojects.com/en/2.10.x/) placeholders in configuration values)

## Concepts

### Configuration variants

#### Basic

With this example:

```ini
[group1]
debug=0
debug[DEV]=1
```

We have two default configuration variant for the `debug` key: the `DEV` one and the default one.

If you don't do anything special, the `debug` value will be `0` (standard default value).

But if you initialize the library with `DEV` as *configuration name*, the `debug` value will be `1`.

Now, if you use `PROD` as *configuration name*, as there is no `debug[PROD]` line/variant,
the debug value will fallback to standard value: `0` (in this example).

#### Inheritance

Still with the same example:

```ini
[group1]
debug=0
debug[DEV]=1
```

What about if we use `DEV_JOHN_MONDAY` as *configuration name* when initializing the library?

As there is no `debug[DEV_JOHN_MONDAY]` line,
one might think that the retained value would be the default one: `0`.

In fact, the retrained value will be `1`! Why? Because `_` (underscore) has a special meaning
in configuration names. This is a kind of inheritance mark.

So `DEV_JOHN_MONDAY` means as a configuration name:

- use `DEV_JOHN_MONDAY` if there is a variant with this exact name
- (else) use `DEV_JOHN` (first level of inheritance) if there is a variant with this name: `DEV_JOHN`
- (else) use `DEV` (second level of inheritance) if there is a variant with this name: `DEV`
- (else) use standard/default value

So with this example:

```ini
[group1]
debug=0
debug[DEV]=1
debug[DEV_JOHN]=2
debug[DEV_PETER]=3
debug[DEV_JOHN_MONDAY]=4
debug[DEV_JOHN_TUESDAY]=5
debug[QA]=6
```

We get this table:

Configuration name | selected value for `debug` key | comment
--- | --- | ---
`FOO` | `0` | standard value is used
`DEV` | `1` | exact variant
`DEV_JOHN_MONDAY` | `4` | exact variant
`DEV_JOHN_FRIDAY` | `2` | `DEV_JOHN` level of inheritance is used
`DEV_PETER` | `3` | exact variant
`DEV_KATE` | `1` | `DEV` level of inheritance is used
`DEV_SMITH_FOO_BAR_1` | `1` | `DEV` level of inheritance is used
`DEV_JOHN_QA` | `2` | `DEV_JOHN` level of inheritance is used
`FOO_QA` | `0` | the `QA` level can be used only if the configuration name begins with `QA`
`QA5` | `0` | the `QA5` variant does not exist and there is no inheritance because there is no `underscore`
`QA_5` | `6` | `QA` level of inheritance

### envtpl usage inside configuration values

FIXME

## Usage

`opinionated_configparser` is just a thin layer over [Python configparser library](https://docs.python.org/3/library/configparser.html). So you use it exactly in the same way.

Just an example:

```python
from opinionated_configparser import OpinionatedConfigParser


TEST_DICT = {
    "section1": {
        "key1": "value1",
        "key1[foo]": "value2",
        "key1[foo_bar]": "value3",
        "key2": "value4"
    },
    "section2": {
        "key3": "value5"
    }
}


parser = OpinionatedConfigParser(configuration_name="foo")
parser.read_dict(TEST_DICT)

# will output: value2
print(parser.get("section1", "key1"))

# [...]
# use the parser object exactly as configparser.ConfigParser one
# [...]
```








## Contributing guide

See [CONTRIBUTING.md](CONTRIBUTING.md) file.



## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) file.



## Sponsors

*(If you are officially paid to work on MetWork Framework, please contact us to add your company logo here!)*

[![logo](https://raw.githubusercontent.com/metwork-framework/resources/master/sponsors/meteofrance-small.jpeg)](http://www.meteofrance.com)
