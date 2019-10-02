from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name="yaml2jupyterhub",
    packages=["yaml2jupyterhub"],
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': ['yaml2jupyterhub=yaml2jupyterhub.main:main'],
    },
)