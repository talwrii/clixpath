import setuptools
import distutils.core
import os

HERE = os.path.dirname(__file__)

setuptools.setup(
    name='clixpath',
    version=0.1,
    author='Tal Wrii',
    author_email='talwrii@gmail.com',
    description='',
    license='GPLv3',
    keywords='',
    url='',
    packages=['clixpath'],
    long_description='See https://github.com/talwrii/clixpath',
    entry_points={
        'console_scripts': ['clixpath=clixpath.clixpath:main']
    },
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Topic :: Text Processing :: Markup :: HTML"
    ],
    test_suite='nose.collector',
    install_requires=['lxml']
)
