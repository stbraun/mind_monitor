from distutils.core import setup

setup(
    name='PyMindMonitor',
    version='0.1.0.dev3',
    packages=['mind_monitor'],
    # package_dir={'': 'mind_monitor'},
    url='https://github.com/stbraun/mind_monitor/tree/master',
    license='MIT',
    author='Stefan Braun',
    author_email='sb@action.ms',
    description='Mindwave interface',
    requires=['matplotlib', 'PyYaml', 'behave', 'pymongo'],
    include_package_data=True,
    package_data=dict(resources=['log_config.yaml', ])
    # entry_points={'console_scripts': ['monitor=monitor:main']}
)
