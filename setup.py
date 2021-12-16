from setuptools import setup, find_packages
setup(
    name="fauxioapi",
    version="0.1",
    packages = find_packages(),
    python_requires='>=3.5',
    setup_requires=['numpy>=1.16','netCDF4>=1.2.9'],
    url="https://github.com/jlbeidler/fauxioapi",
    author_email='james.beidler@gmail.com'
)
