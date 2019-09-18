import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anki_ocr",
    version="0.2",
    author="madelesi",
    author_email="saifemasoud@gmail.com",
    description="Converts physical flashcards to digital anki flashcards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/madelesi/anki_ocr",
    packages=setuptools.find_packages(),
    install_requires=['genanki'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points ={
        'console_scripts': [
            'anki_ocr = anki_ocr.anki_ocr:main'
        ]
    }

)
