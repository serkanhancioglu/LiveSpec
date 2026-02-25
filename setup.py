from setuptools import setup, find_packages

setup(
    name="livespec",
    version="0.1.0",
    description="Automatic live API documentation and request logging for Flask apps",
    author="Serkan Hancioglu",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0",
        "flask-apispec>=0.12.0",
        "apispec>=6.0.0",
        "swagger-ui-bundle>=0.0.9",
    ],
    python_requires=">=3.8",
)
