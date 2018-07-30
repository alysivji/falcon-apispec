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


with open("README.md") as f:
    long_description = f.read()

setup(
    name="falcon-apispec",
    version=find_version("falcon_apispec", "version.py"),

    author="Aly Sivji",
    author_email="alysivji@gmail.com",

    description="Falcon plugin for apispec documentation generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/alysivji/falcon-apispec",

    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="falcon apispec swagger openapi specification documentation spec rest api",

    install_requires=[
        "PyYAML>=3.10",
        "apispec>=1.0.0b1",
        "falcon",
    ],
    packages=find_packages(exclude=["tests", ]),
    test_suite='tests',

    zip_safe=False,
)
