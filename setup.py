# Licensed under MIT License - see LICENSE

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = 'dendrogram',
    packages = find_packages(),
    version = '0.3.dev',
    url = "https://github.com/EnthalpyBill/Dendrogram",
    license = "MIT",
    author = ["Xi Meng", "Bill Chen"],
    author_email = ["xim@umich.edu", "ybchen@umich.edu"],
    maintainer = "Bill Chen",
    maintainer_email = "ybchen@umich.edu",
    description = "A toolkit for creating N-dimensional (ND) dendrogram",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires = ["numpy>=1.18"],
    python_requires = ">=3.8",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)