from setuptools import setup, find_packages


setup(
    name='glicko',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'ax-platform',
        'matplotlib',
        'numpy',
        'python-dateutil',
        'sklearn',
    ],
    tests_require=[
        'pytest',
    ]
)
