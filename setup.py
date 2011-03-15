from distutils.core import setup
from transparencydata import __version__

long_description = open('README.rst').read()

setup(name="python-transparencydata",
      version=__version__,
      py_modules=["transparencydata", "influenceexplorer"],
      description="Library for interacting with the Sunlight Labs Transparency Data API",
      author="Jeremy Carbaugh",
      author_email = "jcarbaugh@sunlightfoundation.com",
      license='BSD',
      url="http://github.com/sunlightlabs/python-transparencydata/",
      long_description=long_description,
      platforms=["any"],
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      )
