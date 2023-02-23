import os

import goslate
import translators as ts
from bs4 import BeautifulSoup

target_language = 'hi'
source_language = 'fr'

gs = goslate.Goslate()

# function to translate the text


def translate_text(target, text):
    soup = BeautifulSoup(text, 'html.parser')
    elements = ['html', 'h1', 'h2', 'h3', 'p',
                'title', 'strong', 'li', 'a', 'button']
    for tag in soup.find_all(string=True):
        if tag != "\n":
            if (len(tag) > 0 and len(tag) < 5000 and isinstance(tag, str)):
                if ";" in tag or "JSON" in tag or "function" in tag or "{" in tag:
                    continue
                else:
                    # translation = gs.translate(tag, target_language)
                    translation = ts.translate_text(
                        query_text=tag, if_ignore_empty_query=True, to_language=target_language, translator='google')
                    if (len(translation) > 0):
                        tag.replace_with(translation)
    return str(soup)


# recursively read all files in the directory and
# subdirectories with ".html" extension
for root, dirs, files in os.walk('../xtras'):
    for file in files:
        if file.endswith('.html'):
            with open(os.path.join(root, file), 'r+', encoding='utf-8') as f:
                data = f.read()
                # print(data)
                # list = ""
                with open('list.txt', 'r') as fi:
                    list = fi.read()
                    fi.close()
                # use googletrans to translate the contents of the file
                translated = translate_text(target_language, data)
                if (len(translated) > 0 and file not in list):
                    print("updating file")
                    # clear the original contents
                    f.truncate(0)
                    # write the translated data back to the file
                    f.write(translated)
                    with open('list.txt', 'a') as fi:
                        print(file + '\n', file=fi)
                        fi.close()
                    f.close()

print("Done!")
