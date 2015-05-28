from setuptools import setup, find_packages

__author__ = 'xuemingli'

def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name='et',
    version="0.1.0",
    license='apache-2',
    author='comyn',
    author_email='me@xueming.li',
    description='Lightweight wrapper for tornado.',
    long_description=readme(),
    url='https://github.com/lixm/yaconf',
    install_requires=[
        "tornado >= 4.2",
    ],
    packages=['yaconf'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
