from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    long_desc = file.read()

setup(
    name='concisys-bom-quoter',
    version='1.0.0',
    author='Lan Do, Monica Nguyen',
    author_email='mnguyen@concisys.net',
    description='Bom Quoter Prototype to calculate best pricing by labor cost and units in a single Excel File.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/concisys-dev0/bom_quoter/",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    install_requires=[
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
        'xlsxwriter>=3.1.1',
        'xlwings>=0.30.10',
        'setuptools>=68.0.0',
    ],
    entry_points={"console_scripts": ["bomquoter=utils.__main__:main"]},
)
