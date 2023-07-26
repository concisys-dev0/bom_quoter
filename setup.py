# import sys
# from pathlib import Path

# file = Path(__file__).resolve()
# parent, root = file.parent, file.parents[1]
# sys.path.append(str(root))

# # Additionally remove the current file's directory from sys.path
# try:
#     sys.path.remove(str(parent))
# except ValueError: # already removed
#     pass
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bom_quoter',
    version='1.0.0',
    author="Lan Do, Monica Huu Nguyen, Concisys Inc.",
    author_email="mnguyen@concisys.net",
    license="MIT",
    url="https://github.com/concisys-dev0/bom_quoter",
    description="A prototype of a bom quoter built on Python",
    long_description=long_description,
    packages=setuptools.find_packages(),
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
    ])
