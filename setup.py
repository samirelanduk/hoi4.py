from setuptools import setup
from glob import glob
import os

with open("README.md") as f:
    long_description = f.read()

setup(
    name="hoi4.py",
    version="0.1.0",
    description="A Hearts of Iron 4 save file parser and analyser.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samirelanduk/hoi4.py",
    author="Sam Ireland",
    author_email="mail@samireland.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="hoi4 save-parser",
    packages=["hoi4"],
    python_requires="!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    install_requires=[]
)