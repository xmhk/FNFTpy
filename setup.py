from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="FNFTpy",
    version="0.1",
    author="Christoph Mahnke",
    author_email="",
    description=("A python wrapper for FNFT, a C library to calculate the "
                 "Nonlinear Fourier Transform listening skills "
                 "while watching movies"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xmhk/FNFTpy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy"
    ]
)
