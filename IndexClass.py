from hashedindex import HashedIndex
from base64 import b64encode
from random import choice
from string import ascii_letters, punctuation
from google.cloud import vision
from timeit import default_timer


class TapSearchAPI:
    def __init__(self):
        self.InvertedIndex = HashedIndex()
        self.count = 0

    @staticmethod
    def word_tokenize(text):
        text = text.translate(str.maketrans(punctuation, ' '*len(punctuation)))
        return text.split(' ')

    def preprocess(self, text, name=''):
        """
        Preprocessing
        text (params): a chunk of text
        para (return): a dict of tokens for indexing
        """
        text = text.replace('\r', '')
        paragraphs = [i.lower() for i in text.split('\n\n')]
        if not name:
            temp_count = len(self.InvertedIndex.documents())
            name = 'Document'
            tagged_tokens = {f'{name} {temp_count+num}': self.word_tokenize(i) for num, i in enumerate(paragraphs)}
        else:
            tagged_tokens = {f'{name} {num}': self.word_tokenize(i) for num, i in enumerate(paragraphs)}
        self.count += len(paragraphs)
        return tagged_tokens

    def index(self, text, name=None):
        """
        Making an index
        tag_tokens (param): a dict of tokens with names
        None (return):
        """
        initial_time = default_timer()
        tag_tokens = self.preprocess(text, name)
        for key in tag_tokens:
            for token in tag_tokens[key]:
                self.InvertedIndex.add_term_occurrence(token, key)
        print(f'Time elapsed: {default_timer() - initial_time}')
        return "Indexed"

    def clear(self):
        """
        Deleting all values in Index
        """
        self.InvertedIndex = HashedIndex()
        return 'Cleaned Index'

    def search(self, keyword):
        """
        Searching in the index for the given keyword
        keyword (param): a string given
        results (return): a list of occurences in InvertedIndex for keyword
        """
        keyword = keyword.lower()
        if keyword in self.InvertedIndex:
            return self.InvertedIndex[keyword].most_common(10)
        else:
            return {}

    def image(self, img):
        """
        Converts image to text in GCP and indexes the text
        img (param): Image file buffer
        None (return)
        """
        client = vision.ImageAnnotatorClient()
        with open(img, 'rb') as image_file:
            content = image_file.read()
        encoded = b64encode(content)
        image = vision.types.Image(content=encoded)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        print(texts)

    @staticmethod
    def char_generate():
        """
        To avoid duplicate file name collision, I add two random char if file already uploaded to its name
        gen (return): Two random generate char
        """
        return ' '+choice(ascii_letters)+choice(ascii_letters)
