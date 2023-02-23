from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="hexgen",
    description="Realistic world generation via a hexmap for RPGs",
    packages=find_packages(),
    install_requires=required,
)
