
# anki_ocr

anki_ocr is a python program that converts physical flashcards into digital [Anki](https://apps.ankiweb.net)(Anki is a flashcard program that sychronizes your flashcards and uses spaced repetition for efficient memorization) decks. It uses [PyTesseract](https://pypi.org/project/pytesseract/) and [genanki](https://github.com/kerrickstaley/genanki) to turn your handwritten flashcards into digital anki ones.

There are several use cases, mainly its for you if you have a lot of flashcards and and want to digitize them. Anki does support image flashcards, but it would take a lot of time and you wouldn't be able to search the flashcards. Its also useful if you're not allowed to use a laptop/phone in class or prefer to handwrite your notes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install anki_ocr.

```bash
pip install anki_ocr
```

## Usage
To use anki_ocr, you will need a directory with images of your flashcards. The program will automatically sort the images by date, so you should **capture the question followed by its answer(i.e question1>answer1>question2>answer2 and so on), and ensure the number of images is even**

```bash
anki_ocr [img_directory] [output_deck_name]
```

This will output an Anki deck package output_deck_name.apkg. This package can be imported into the Desktop or mobile Anki apps

## Contributing
This project is beginner friendly. The entire module is a small single file, and the only new package you might have to deal with is genanki just to see some other ways to generate notes.

Clone the project & you probably want a virtual environment
```bash
git clone https://github.com/madelesi/anki_ocr.git
cd anki_ocr
python3 -m venv venv_anki_ocr
source venv_anki_ocr/bin/activate
```
Then install an editable version (updates after every save)
```bash
pip install -e .
```


Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)