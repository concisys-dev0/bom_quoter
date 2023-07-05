import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='src',
    version='1.0.0',
    author="Lan Do, Monica Huu Nguyen, Concisys Inc.",
    author_email="mnguyen@concisys.net",
    license="MIT",
    url="https://github.com/concisys-dev0/bom_quoter",
    description="Concisys BOM Quoter",
    long_description=long_description,
    packages=setuptools.find_packages(exclude=['tests','notebooks']),
    include_package_data=True,
    install_requires=[
        'python>=3.10.11',
        'requests>=2.31.0',
        'requests-oauthlib>=1.3.1',
        'schedule>=1.2.0',
        'selenium>=4.9.1',
        'numpy>=1.23.5',
        'oauthlib>=3.2.2',
        'openpyxl>=3.0.10',
        'pandas>=1.5.3',
        'urllib3>=2.0.3',
        'webdriver-manager>=3.8.6',
    ],
     )