from setuptools import setup, find_packages


setup(
    name='data-sitter',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        # Keep this in sync with pyproject.toml
        "python-dotenv==1.0.1",
        "PyYAML==6.0.2",
        "parse_type==0.6.4",
        "pydantic==2.10.5",
    ],
    entry_points={
        'console_scripts': [
            'data-sitter=data_sitter.cli:main',
        ],
    },
)
