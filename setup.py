from setuptools import setup, find_packages

setup(
    name='WeSchedule',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'study-group-scheduler=scheduler.scheduler:suggest_time',
        ],
    },
    description='A tool to schedule study group sessions based on availability.',
    author='egpz',
    license='MIT',
)
