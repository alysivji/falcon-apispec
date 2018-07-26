from setuptools import setup, find_packages

setup(
    name="falcon-apispec",
    version="0.0.1",
    description="Falcon plugin for apispec documentation generator.",
    url="https://github.com/alysivji/falcon-apispec",
    author="Aly Sivji",
    author_email="alysivji@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.6" "Programming Language :: Python :: 3.7"
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=["falcon", "apispec"],
    download_url="https://github.com/alysivji/falcon-apispec",
)
