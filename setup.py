from setuptools import setup, find_packages

setup(
    name="snapscan-core",
    version="0.1.0",
    description="Lightweight cross-platform screenshot QR code scanner library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["snapscan_core"]),
    install_requires=[
        "mss",
        "pyzbar",
        "Pillow",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)