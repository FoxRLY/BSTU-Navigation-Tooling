from os import listdir
from os.path import isfile
import json
import base64


if __name__ == "__main__":
    images: list[dict[str, str]] = list()
    file_names = [file_name for file_name in listdir(r"./images/")
                  if isfile(r"./images/"+file_name)
                  and file_name.endswith(".png")]

    for file_name in file_names:
        with open(r"./images/"+file_name, "rb") as image:
            raw_image = image.read()
            encoded_image = base64.b64encode(raw_image).decode("utf-8")
            images.append({"name":file_name, "value":encoded_image})
    
    result = json.dumps(images);
    with open(r"./jsons/images.json", "w") as dump:
        dump.write(result)

