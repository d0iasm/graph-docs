import re
import sys
from bs4 import BeautifulSoup


removed_files = []
files = sys.argv

def nc_data():
    for i in range(1, len(files)):
        content = []
        with open(files[i]) as f:
            for line in f:
                text = re.sub(r'[F|M][0-9]{3}：', '', line.strip())
                text = re.sub(r'（.*）', '', text)
                text = re.sub(r'＜.*＞', '', text)
                content.append(text)
        removed_files.append(content)

        
def livedoor_data():
    for i in range(1, len(files)):
        content = []
        with open(files[i]) as f:
            for line in f:
                soup = BeautifulSoup(line.strip(), 'html.parser')
                content.append(soup.text + '\n')
        removed_files.append(content)


def save_files():
    for i in range(1, len(files)):
        with open('after_'+files[i], mode='w', encoding='utf-8') as f:
            f.writelines(removed_files[i-1])


if files[1] == 'livedoor-news-data.txt':
    livedoor_data()
else:
    nc_data()
save_files()
