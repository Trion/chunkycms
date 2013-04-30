from setuptools import setup

setup(
    name='chunkycms',
    version='0.1',
    install_requires=[
        "Django>=1.4",
    ],
    tests_require=["Django"],
    test_suite="run_tests.main",
)
