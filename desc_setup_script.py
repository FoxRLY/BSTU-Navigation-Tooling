import requests
from os import listdir
from os.path import isfile
import json
from bs4 import BeautifulSoup, NavigableString

if __name__ == "__main__":
    image_names = [file_name for file_name in listdir(r"./images/")
                   if isfile(r"./images/"+file_name)
                   and file_name.endswith(".png")]

    image_mapping = {"ГУК": "GUK",
                     "УК1": "UK1",
                     "УК2": "UK2",
                     "УК3": "UK3",
                     "УК4": "UK4",
                     "УК6": "UK6"}
    url = r"https://t.bstu.ru/raspisaniya/auditorii"
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:110.0) Gecko/20100101 Firefox/110.0"}
    try:
        response = requests.get(url, headers=header)
    except Exception as e:
        print("Error: {e}")
        exit()
    if not response.ok:
        print("Bruh, server denied")
        exit()
    soup = BeautifulSoup(response.text, features="lxml")
    table = soup.find("div", class_="_tab-content tab-content active")
    if not table:
        print("Parsing failed")
        exit()
    classrooms_raw = table.find_all("a", class_="teachers__item")
    classrooms_names = [name.text for name in classrooms_raw]
    
    data_entries = []
    for classroom in classrooms_names:
        entry = dict()
        entry["classroom"] = classroom
        classroom_prefix = classroom.split()[0]
        mapped_classroom_prefix = image_mapping.get(classroom_prefix)
        if mapped_classroom_prefix:
            entry["images"] = [name for name in image_names
                               if name.startswith(mapped_classroom_prefix)]
        else:
            entry["images"] = []
        entry["description"] = "Описание еще не добавлено"
        data_entries.append(entry)

    result = json.dumps(data_entries)
    with open(r"./jsons/classrooms.json", "w") as dump:
        dump.write(result)

