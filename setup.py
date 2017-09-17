from setuptools import setup, find_packages

setup(
    name='tornado_instant_webapi',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/Hiroshiba/tornado_instant_webapi',
    author='Kazuyuki Hiroshiba',
    author_email='hihokaruta@gmail.com',
    description='The library for automatically generating web API from Python object based on Tornado.',
    license='MIT License',
    install_requires=[
        'tornado',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ]
)
