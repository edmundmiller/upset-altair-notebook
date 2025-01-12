from setuptools import setup, find_packages

setup(
    name="altair-upset",
    version="0.1.0",
    description="Create UpSet plots using Altair",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "altair>=5.0.0",
        "pandas>=1.0.0"
    ],
    python_requires=">=3.8",
) 