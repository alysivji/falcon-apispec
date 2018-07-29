import codecs
import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="falcon-apispec",
    version=find_version("falcon_apispec", "__version__.py"),
    description="Falcon plugin for apispec documentation generator.",
    url="https://github.com/alysivji/falcon-apispec",
    author="Aly Sivji",
    author_email="alysivji@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=["falcon", "apispec"],
    download_url="https://github.com/alysivji/falcon-apispec",
)
