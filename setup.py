from setuptools import setup

with open("README.md", "r") as file:
    readme_content = file.read()

setup(
    name = "bigjpg",
    version = "1.1.0",
    license = "MIT License",
    author = "Marcuth",
    long_description = readme_content,
    long_description_content_type = "text/markdown",
    author_email = "marcuth2006@gmail.com",
    keywords = "bigjpg wrapper api",
    description = f"Wrappper for https://bigjpg.com/",
    packages = ["bigjpg", "bigjpg/types"],
    install_requires = ["requests", "pydantic"],
)