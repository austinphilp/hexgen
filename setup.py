from setuptools import find_packages, setup

setup(
    name="hexgen",
    description="Realistic world generation via a hexmap for RPGs",
    packages=find_packages(),
    install_requires=[
        "Pillow==9.4.0",
        "NumPy==1.24.2",
    ],
)
