"""Converts an image directory into an anki Deck in a .apkg file. """
import os
import sys
import argparse
import random
from pathlib import Path
import genanki


img_file_extensions = [".jpg", ".png", ".gif", ".tiff", ".svg", ".tif", ".jpeg", ".mp3", ".ogg", ".wav", ".avi", ".ogv", ".mpg", ".mpeg", ".mov", ".mp4", ".mkv",
                       ".ogx", ".ogv", ".oga", ".flv", ".swf", ".flac", ".webp", ".m4a"]


def main(img_dir=None, deck_name=None, ocr=False):
    """ Converts img_dir to an anki deck

    Args:
        img_dir: A directory with images forming question/answer pairs
        deck_name: Name of the outputted anki .apkg file.
        ocr: Convert image to text through OCR.
    """
    if img_dir == None:  # In other words, if run from command-line
        args = parse_arguments()
        img_dir, deck_name, ocr = args.img_dir, args.deck_name, args.ocr

    # Get path for images folder
    img_path_object = Path(img_dir)
    print(
        f"img_dir={img_path_object.absolute()}\ndeck={deck_name}\nocr={ocr}\n")

    # Group Directory to Q,A pairs
    q_a_pairs = pair_images(img_path_object)

    # Initialize deck and add notes
    deck_id = random.randrange(1 << 30, 1 << 31)
    media_files = []
    deck = genanki.Deck(deck_id, deck_name)

    # convert Q, A image pair to text(through OCR)
    if ocr:
        q_a_text_pairs = convert_q_a_pairs(q_a_pairs)
        add_tuples_anki_deck(deck, q_a_text_pairs)

    if not ocr:
        # We have to store all media files in a list to add them to our anki package.
        for q_path, a_path in q_a_pairs:
            media_files.append(str(q_path))
            media_files.append(str(a_path))
        add_tuples_anki_deck(deck, q_a_pairs, media=True)

    # save deck to output file
    save_anki_deck(deck, media_files)


def save_anki_deck(deck: genanki.Deck, media_files: list):
    pkg = genanki.Package(deck)
    pkg.media_files = media_files
    pkg.write_to_file(f'{deck.name}.apkg')
    print(f'conversion complete, packaged to {deck.name}.apkg')


def parse_arguments():
    """ Parses CLI arguments

    Returns:
        Tuple: main script arguments
    """
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
    """Converts pairs of images to pairs of text

    Args:
        q_a_pairs (PosixPath tuple list):

    Returns:
        List of tuples.
    """
    q_a_text_pairs = []
    for q, a in q_a_pairs:
        q_a_text_pair = image_to_text(q), image_to_text(a)
        q_a_text_pairs.append(q_a_text_pair)
    return q_a_text_pairs


def add_tuples_anki_deck(anki_deck, tuples_list, media=False):
    """Adds q&a tuple pairs to anki deck

    Args:
        anki_deck (Deck object):
        tuples_list (List):
        media (bool):
    """
    if not media:
        for q_text, a_text in tuples_list:
            add_note_anki_deck(anki_deck, q_text, a_text)
    if media:
        for q_file, a_file in tuples_list:
            add_img_note_anki_deck(anki_deck, q_file, a_file)


def pair_images(img_path_object):
    """Pairs images in a given PosixPath directory

    Args:
        img_path_object(pathlib Path)

    Returns:
        List of tuples(pairs) of pathlib Paths

    Raises:
        ValueError if number of images isn't even.
    """
    # Make Sure all files in directory are images (JPEG/PNG)
    img_list = []
    for img in img_path_object.iterdir():
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
    """Pairs elements of list into tuples of pair_length

    Args:
        list_to_pair (List)
        pair_length (int)

    Returns:
        List of tuples
    """
    # Create N copies of the same iterator
    it = [iter(list_to_pair)] * pair_length
    # Unpack the copies of the iterator, and pass them as parameters to zip
    return list(zip(*it))


def image_to_text(filepath):
    """Converts an image file into text

    Args:
        filepath (string): filepath of the image

    Returns:
        String: Text of the image

    Raises:
        Exception: If OCR requirements aren't available
    """
    try:
        import pytesseract
        from PIL import Image
        text = pytesseract.image_to_string(Image.open(filepath))
        return text
    except ImportError:
        raise Exception(
            'To use OCR you need to install pytesseract & Pillow:\n pip install pytesseract pillow')


def add_note_anki_deck(deck, q_text, a_text):
    """Adds a note to a genanki deck object.

    Args:
        deck (genanki Deck)
        q_text (string)
        a_text (string)
    """
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
    print(f'Added note: q_text: {q_text}, a_text: {a_text}')


def add_img_note_anki_deck(deck, q_file, a_file):
    """adds an image note to a genanki Deck

    Args:
        deck (genanki Deck)
        q_file (string): Path of question image
        a_file (string): Path of answer image
    """
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
    my_note = genanki.Note(model=my_model, fields=[
                           f"<img src={q_file.name}>", f"<img src={a_file.name}>"])
    deck.add_note(my_note)
    print(f'-Added note with q_img: {q_file.name}, a_img: {a_file.name}')


if __name__ == '__main__':
    main()
