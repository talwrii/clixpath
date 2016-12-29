import setuptools
import distutils.core

setuptools.setup(
    name='clixpath',
    version=0.1,
    author='Tal Wrii',
    author_email='talwrii@gmail.com',
    description='',
    license='GPLv3',
    keywords='',
    url='',
    packages=[],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['clixpath=clixpath.clixpath:main']
    },
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Topic :: Text Processing :: Markup :: HTML"
    ],
    test_suite='nose.collector'
)
