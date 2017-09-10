try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import nosql_versioning

with open("README.rst") as readme_file:
    readme_string = readme_file.read()

setup(
    name="nosql_versioning",
    version=nosql_versioning.__version__,
    description="Python Library for NoSQL database record versioning",
    author="Xin Huang",
    author_email="xinhuang.abc@gmail.com",
    url="https://github.com/xinhuang/nosql_versioning",
    packages=['nosql_versioning', 'tests'],
    license="License :: OSI Approved :: MIT License",
    long_description=readme_string,
)
