from setuptools import setup, find_packages

setup(
    name="dsl-automacao",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "lark-parser==0.12.0",
    ],
    python_requires=">=3.8",
) 