import os

from bs4 import BeautifulSoup
from googletrans import Translator

target_language = 'hi'
source_language = 'en'

# function to translate the text


def translate_text(target, text):
    translator = Translator()
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all(string=True):
        if tag != "\n":
            translation = translator.translate(
                tag, src=source_language, dest=target).text
            tag.replace_with(translation)
    return str(soup)


# recursively read all files in the directory and
# subdirectories with ".html" extension
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            with open(os.path.join(root, file), 'r+') as f:
                data = f.read()
                # use googletrans to translate the contents of the file
                translated = translate_text(target_language, data)
                # write the translated data back to the file
                # clear the original contents
                f.truncate(0)
                with open(file, 'w'):
                    f.write(translated)
