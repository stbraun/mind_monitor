import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """This is a plug-in for setuptools.

     It will invoke py.test when you run python setup.py test
    """
    def finalize_options(self):
        """Configure."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Execute tests."""
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = '0.1.0.dev4'

setup(
    name='PyMindMonitor',
    version=version,
    url='https://github.com/stbraun/mind_monitor',
    license='MIT',
    author='Stefan Braun',
    author_email='sb@action.ms',
    description='Mindwave interface',
    long_description=open("README.rst").read(),
    include_package_data=True,
    package_data=dict(resources=['log_config.yaml', ]),

    classifiers=[  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers TASK
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing'
    ],
    keywords="development tools",  # Separate with spaces TASK
    packages=find_packages(exclude=['test']),
    zip_safe=False,
    cmdclass={'test': PyTest},

    provides=['mind_monitor'],
    app=["monitor_app.py"],  # TASK

    # List of packages that this one depends upon:
    requires=['numpy', 'matplotlib', 'PyYaml', 'pyzmq', 'genutils'],
    setup_requires=["py2app"],
    tests_require=['behave', 'nose', 'pytest'],
    install_requires=['setuptools'],

)
