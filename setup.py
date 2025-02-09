from setuptools import find_packages, setup

setup(
    name='hsm-py',
    packages=find_packages(include=['hsm']),
    version='1.3.0',
    description='A hierarchical state machine implemented in Python',
    author='julian.krumow@artcom.de',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.3.4'],
    test_suite='tests',
)
