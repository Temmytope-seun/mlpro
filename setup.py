from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path:str)->List[str]:
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements

setup(
    name="mlpro",
    version="0.0.1",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    author="Temmy",
    author_email="temmytope60@gmail.com"
)