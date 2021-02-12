import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="movies_map-Yuriy-Sukhorskyy",
    version="0.0.1",
    author="Yuriy-Sukhorskyy",
    author_email="yurii.sukhorskyi@ucu.edu.ua",
    description="Laboratory work №2 - Task #2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)