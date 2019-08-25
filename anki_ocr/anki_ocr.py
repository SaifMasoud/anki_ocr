from pathlib import Path
import sys
import pytesseract
from PIL import Image
import random
import genanki
import os

img_file_extensions = ['.png', '.jpg']


def main():

    # Verify correct number of arguments
    try:
        img_dir_name = sys.argv[1]
        deck_name = sys.argv[2]
    except IndexError:
        raise ValueError('Usage: python anki_ocr_py img_directory deck_name')

    # Get path for images folder
    img_path = Path(img_dir_name)

    # Group Directory to Q,A pairs
    q_a_pairs = pair_images(img_path)

    # convert Q, A image pair to text(through OCR)
    q_a_text_pairs = []
    for q, a in q_a_pairs:
        q_a_text_pair = image_to_text(q), image_to_text(a)
        q_a_text_pairs.append(q_a_text_pair)

    # Initialize deck and add notes
    deck_id = random.randrange(1 << 30, 1 << 31)
    my_deck = genanki.Deck(deck_id, deck_name)
    for q_text, a_text in q_a_text_pairs:
        add_note_anki_deck(my_deck, q_text, a_text)

    # Package deck to output file
    genanki.Package(my_deck).write_to_file(f'{deck_name}.apkg')


def pair_images(img_path):
    # Make Sure all files in directory are images (JPEG/PNG)
    img_list = []
    for img in img_path.glob('*'):
        if img.suffix not in img_file_extensions:
            raise ValueError(
                'All files in image directory must be PNG/JPEG format')
        img_list.append(img)

    # Sort img_list
    img_list.sort(key=os.path.getmtime)

    # Verify an even number of images to create pairs
    if len(img_list) % 2 != 0:
        raise ValueError('Number of images must be even(multiple of 2)')
    q_a_pairs = list_to_tuples(img_list, 2)
    return q_a_pairs


def list_to_tuples(list_to_pair, pair_length):
    # Create N copies of the same iterator
    it = [iter(list_to_pair)] * pair_length
    # Unpack the copies of the iterator, and pass them as parameters to zip
    return list(zip(*it))


def image_to_text(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text


def add_note_anki_deck(deck, q_text, a_text):
    # Basic anki note model
    model_id = random.randrange(1 << 30, 1 << 31)
    my_model = genanki.Model(
        model_id,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    my_note = genanki.Note(model=my_model, fields=[q_text, a_text])
    deck.add_note(my_note)


if __name__ == '__main__':
    main()
