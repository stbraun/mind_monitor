from distutils.core import setup

setup(
    name='PyMindMonitor',
    version='0.0.1dev',
    packages=[''],
    package_dir={'': 'mind_monitor'},
    url='https://bitbucket.org/sb_/pymindmonitor',
    license='MIT',
    author='Stefan Braun',
    author_email='sb@action.ms',
    description='Mindwave interface',
    requires=['matplotlib', 'PyYaml']
)
