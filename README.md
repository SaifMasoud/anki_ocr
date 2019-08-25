# anki_ocr

anki_ocr is a python program that converts physical flashcards into digital [Anki](https://apps.ankiweb.net)(Anki is a flashcard program that sychronizes your flashcards and uses spaced repetition for efficient memorization) decks. It uses [PyTesseract](https://pypi.org/project/pytesseract/) and [genanki](https://github.com/kerrickstaley/genanki) to turn your handwritten flashcards into digital anki ones.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install anki_ocr.

```bash
pip install anki_ocr
```

## Usage
To use anki_ocr, you will need a directory with images of your flashcards. The program will automatically sort the images by date, so you should **capture the question followed by its answer, and ensure the number of images is even**

```bash
anki_ocr [img_directory] [output_deck_name]
```

This will output an Anki deck package output_deck_name.apkg. This package can be imported into the Desktop or mobile Anki apps

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)