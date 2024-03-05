import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoui",
    version="0.0.1",
    author="CTO",
    author_email="firedcto@gmail.com",
    description="Automation with Computer Vision for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrashTechnologyOfficer/autoui",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.4',
)
