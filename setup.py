"""
https://pypi.org/project/setuptools-scm/
w pliku o_mnie.py wykorzystano wersjonowanie.
setuptools_scm wykorzystuje tagowanie wersji w .git
"""
from setuptools import setup

setup(
    name='Projekt Bez Polskich Znaków',
    packages=[],
    url='https://github.com/Lioheart/Projekt_Bez_Polskich_Znakow',
    license='MIT',
    author='Jakub Hawro',
    author_email='',
    description='Program na wewnętrzne potrzeby Kuźni Jawor',
    requires=['PyQt5', 'openpyxl', 'XlsxWriter', 'Pillow', 'dropbox'],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
