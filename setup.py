from setuptools import setup, find_packages

setup(
    name='WeSchedule',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'google-api-python-client',
    ],
    entry_points={
        'console_scripts': [
            'study-group-scheduler=scheduler.scheduler:suggest_time',
        ],
    },
    description='A tool to schedule group study sessions and create calendar events.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
