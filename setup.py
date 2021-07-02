from setuptools import setup, find_packages

setup(
    name="image-app",
    version="0.1.0",
    description="Setting up a python package",
    author="Branislav Andjelic, Dusan Milunovic",
    author_email="branislav.andjelic@uns.ac.rs",
    packages=find_packages(),
    tests_require=["pytest"],
    install_requires=[
        "flask",
        "flask-cors",
    ],
    entry_points={
        "console_scripts": [
            "start_server=app.app:main",
        ]
    },
)
