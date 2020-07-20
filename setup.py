import pathlib
from glob import glob

import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="empty-trash",
    version="0.1.0",
    url="https://github.com/edina/nb_empty_trash",
    author="ian Stuart",
    description="Simple Jupyter extension to show the size of the trash folder, and a button the empty it.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    install_requires=["notebook>=6.0.0", "prometheus_client", "psutil>=5.6.0"],
    extras_require={
        "dev": [
            "autopep8",
            "pytest",
            "flake8",
            "pytest-cov>=2.6.1",
            "mock",
            "black",
            "tornado",
            "traitlets",
            "notebook",
            "prometheus_client",
            "pre-commit",
            "psutil>=5.6.0",
        ]
    },
    data_files=[
        ("share/jupyter/nbextensions/empty_trash", ["empty_trash/static/trash.js"]),
        (
            "etc/jupyter/jupyter_notebook_config.d",
            ["jupyter-config/nbconfig/notebook.d/empty_trash.json"],
        ),
        (
            "etc/jupyter/nbconfig/notebook.d",
            ["jupyter-config/jupyter_notebook_config.d/empty_trash.json"],
        ),
    ],
    zip_safe=False,
    include_package_data=True,
)
