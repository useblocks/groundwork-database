"""
groundwork-database
===================
"""
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
version_file = 'groundwork_database/version.py'

with open(version_file, 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='groundwork-database',
    version=version,
    url='http://groundwork-database.readthedocs.org',
    license='MIT license',
    author='useblocks',
    author_email='info@useblocks.com',
    description="Package for hosting groundwork apps and plugins like gwsql_app or gwsql_plugin.",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    install_requires=['groundwork', 'sqlalchemy', 'sphinx', 'gitpython'],
    tests_require=['pytest', 'pytest-flake8'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Topic :: Database',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'groundwork.plugin': ["groundwork_database = "
                              "groundwork_database.plugins.gwdatabase_plugin:"
                              "GwDatabasePlugin"],
    }
)
