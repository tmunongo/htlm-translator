import os

import translators as ts
from bs4 import BeautifulSoup

target_language = 'hi'
source_language = 'fr'

# function to translate the text


def translate_text(target, text):
    soup = BeautifulSoup(text, 'html.parser')
    # ['html', 'body', 'h1', 'h2', 'h3', 'p', 'title', 'strong', 'li', 'a', 'button']
    for tag in soup.find_all(string=True):
        if tag != "\n":
            if (len(tag) > 0 and len(tag) < 5000 and isinstance(tag, str)):
                if ";" in tag or "JSON" in tag or "function" in tag or "{" in tag:
                    continue
                else:
                    translation = ts.translate_text(
                        query_text=tag, if_ignore_empty_query=True, to_language=target, translator='google')
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
                print(data)
                # use googletrans to translate the contents of the file
                translated = translate_text(target_language, data)
                if (len(translated) > 0):
                    print("updating file")
                    # clear the original contents
                    f.truncate(0)
                    # write the translated data back to the file
                    f.write(translated)
                    f.close()

print("Done!")
