"""Main setup script."""

import setuptools  # type: ignore

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pineboo",
    version="0.12",
    author="David Martínez Martí",  # FIXME: How do we add more authors here?
    author_email="deavidsedice@gmail.com",
    description="ERP replacement for Eneboo written in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deavid/pineboo",
    packages=setuptools.find_packages(),
    package_data={"pineboolib": ["py.typed"]},
    keywords="erp pineboo eneboo accounting sales warehouse",
    python_requires="~=3.6",
    entry_points={
        "console_scripts": [
            "pineboo-parse=pineboolib.application.parsers.qsaparser.postparse:main",
            "pineboo-pyconvert=pineboolib.application.parsers.qsaparser.pyconvert:main",
            "pineboo-core=pineboolib.loader.main:startup_no_X",
            "pineboo=pineboolib.loader.main:startup",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Typing :: Typed",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
    ],
)
