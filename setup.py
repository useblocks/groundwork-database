"""
groundwork_sql
==============
"""
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('groundwork_sql/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='groundwork-sql',
    version=version,
    url='http://gwsql.readthedocs.org',
    license='MIT license',
    author='groundwork-sql',
    author_email='info@useblocks.com',
    description="Package for hosting groundwork apps and plugins like gwsql_app or gwsql_plugin.",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    setup_requires=['pytest-runner', 'sphinx', 'gitpython'],
    tests_require=['pytest', 'pytest-flake8'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': ["gwsql = "
                            "groundwork_sql.applications.gwsql_app:start_app"],
        'groundwork.plugin': ["groundwork_sql = "
                              "groundwork_sql.plugins.gwsql_plugin:"
                              "GwSqlPlugin"],
    }
)
