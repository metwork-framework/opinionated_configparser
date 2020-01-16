import sys
from setuptools import setup, find_packages

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n')
        if (line and not line.startswith('--')) and (";" not in line)
    ]
if sys.version_info[:2] < (3, 5):
    install_requires.append("configparser>=3.7.4")

setup(
    name="opinionated_configparser",
    version="0.0.1",
    license="MIT",
    url="https://github.com/metwork-framework/opinionated_configparser",
    description="opinionated python configparser library override to deal "
    "with configuration variants (PROD, DEV...)",
    packages=find_packages(),
    install_requires=install_requires,
)
