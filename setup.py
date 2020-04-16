import setuptools

with open("README.md", "r") as rm:
    long_description = rm.read()

setuptools.setup(
    name="error-explainer",
    version="0.8",
    description="Custom messages for errors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kaarel Loide",
    author_email="kaarel.loide@gmail.com",
    url="https://github.com/K44rel/error-explainer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
