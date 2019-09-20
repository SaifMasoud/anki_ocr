import os
import sys
import argparse
import random
from pathlib import Path
import genanki


img_file_extensions = ['.png', '.jpg']


def main(img_dir=None, deck_name=None, ocr=False):

    if img_dir == None:  # In other words, if run from command-line
        args = parse_arguments()
        img_dir, deck_name, ocr = args.img_dir, args.deck_name, args.ocr

    # Get path for images folder
    img_path_object = Path(img_dir)

    # Group Directory to Q,A pairs
    q_a_pairs = pair_images(img_path_object)

    # Initialize deck and add notes
    deck_id = random.randrange(1 << 30, 1 << 31)
    media_files = []
    my_deck = genanki.Deck(deck_id, deck_name)

    # convert Q, A image pair to text(through OCR)
    if ocr:
        q_a_text_pairs = convert_q_a_pairs(q_a_pairs)
        add_tuples_anki_deck(my_deck, q_a_text_pairs)

    if not ocr:
        # We have to store all media files in a list to add them to our anki package.
        for q_path, a_path in q_a_pairs:
            media_files.append(str(q_path.absolute()))
            media_files.append(str(a_path.absolute()))
        add_tuples_anki_deck(my_deck, q_a_pairs, media=True)

    # Package deck to output file
    my_package = genanki.Package(my_deck)
    my_package.media_files = media_files
    my_package.write_to_file(f'{deck_name}.apkg')
    print(f'conversion complete, packaged to {deck_name}.apkg')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='convert images to anki flashcards.')
    parser.add_argument('img_dir',
                        help='images directory with questions & answers.')
    parser.add_argument('deck_name',
                        help='The name you want for the output package.')
    parser.add_argument('--ocr', default=False, action='store_true',
                        help='Convert the images to text through OCR. (Good Handwriting required)')
    return parser.parse_args()


def convert_q_a_pairs(q_a_pairs):
    q_a_text_pairs = []
    for q, a in q_a_pairs:
        q_a_text_pair = image_to_text(q), image_to_text(a)
        q_a_text_pairs.append(q_a_text_pair)
    return q_a_text_pairs


def add_tuples_anki_deck(anki_deck, tuples_list, media=False):
    if not media:
        for q_text, a_text in tuples_list:
            add_note_anki_deck(anki_deck, q_text, a_text)
    if media:
        for q_file, a_file in tuples_list:
            add_img_note_anki_deck(anki_deck, q_file, a_file)


def pair_images(img_path_object):
    # Make Sure all files in directory are images (JPEG/PNG)
    img_list = []
    for img in img_path_object.glob('*'):
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
    try:
        import pytesseract
        from PIL import Image
        text = pytesseract.image_to_string(Image.open(filename))
        return text
    except ImportError:
        raise Exception(
            'To use OCR you need to install pytesseract & Pillow:\n pip install pytesseract pillow')


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
    print(f'just added note with q_text: {q_text}, a_text: {a_text}')


def add_img_note_anki_deck(deck, q_file, a_file):
    model_id = random.randrange(1 << 30, 1 << 31)
    my_model = genanki.Model(
        model_id,
        'Simple Model with Media',
        fields=[
            {'name': 'QuestionImage'},
            {'name': 'AnswerImage'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{QuestionImage}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{AnswerImage}}',
            },
        ])
    my_note = genanki.Note(model=my_model, fields=[f"<img src={q_file.name}>", f"<img src={a_file.name}>"])
    deck.add_note(my_note)
    print(f'Just added note with q_img: {q_file.name}, a_img: {a_file.name}')


if __name__ == '__main__':
    main()
