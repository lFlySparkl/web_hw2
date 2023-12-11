from setuptools import setup, find_namespace_packages

setup(name = "book_helper",
      version = "0.1.4",
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['book_helper = final_project.main:main']})