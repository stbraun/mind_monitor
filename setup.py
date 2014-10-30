from distutils.core import setup

setup(
    name='PyMindMonitor',
    version='0.1.0.dev1',
    packages=['mind_monitor'],
    # package_dir={'': 'mind_monitor'},
    url='https://bitbucket.org/sb_/pymindmonitor',
    license='MIT',
    author='Stefan Braun',
    author_email='sb@action.ms',
    description='Mindwave interface',
    requires=['matplotlib', 'PyYaml', 'behave'],
    package_data={'resources': ['log_config.yaml',],}
    # entry_points={'console_scripts': ['monitor=monitor:main']}
)
