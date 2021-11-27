import setuptools

# For version number interpretation see: https://semver.org
VERSION = '1.0.0'

required_modules = [
    "Flask==1.1.1",
    "gunicorn==20.0.4",
    "digi-xbee==1.4.0",
    "dictdiffer==0.9.0"]

setuptools.setup(name='Router',
                 version=VERSION,
                 description='',
                 url='',
                 author='',
                 author_email='',
                 license='Private',
                 packages=setuptools.find_packages(where="src"),
                 package_dir={"": "src"},
                 zip_safe=False,
                 entry_points={
                     'console_scripts': ['start_router=app.main:start_app'],
                 },
                 install_requires=required_modules)
