from setuptools import setup, find_packages

setup(
    name='Concisys BOM Quoter',
    version='1.0.0',
    author='Lan Do, Monica Nguyen',
    author_email='mnguyen@concisys.net',
    description='Bom Quoter Prototype to calculate best pricing by labor cost and units in a single Excel File.',
    packages=find_packages(),
    include_package_data=True,
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
)
