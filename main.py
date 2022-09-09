import math
import json
import random
from glob import glob
from typing import List, Optional, Tuple
from PIL import Image

def get_random_background_image() -> Image:
    return Image.open(random.choice(glob("images/Backgrounds/*.png")))

def get_random_image(path: str, excludes: List[str] = [], filter: str = None) -> Optional[Tuple[int, str]]:

    files = set(glob(f"images/{path}/*.png"))

    weights = [int(file.split('/')[-1].split()[0]) for file in list(files)]

    try:
        file_ = random.choices(population=list(files), weights=weights, k=1)[0]
    except IndexError:
        raise IndexError

    if filter:
        files = set(glob(f"images/{path}/*{filter}*.png"))

    excludes = [exclude for exclude in excludes if exclude]
    for exclude in excludes:
        files -= set(glob(f"images/{path}/*{exclude}.png"))

    if file_ in list(files):
        return int(file_.split('/')[-1].split()[0]), file_

    return None, None


order = [
    "Back details",
    "Bases",
    "Insides",
    "Face details",
    "Eyes",
    "Chin traits",
    "Armor",
    "Animal details",
    "Helmet traits"
]

animal_details = [
    "Cat details",
    "Centipede details",
    "Dragon details",
    "Wolf details",
]

used_data = []

used_traits = []

amount = 0

delimeter = math.pow(100, 10)

i = 0
while amount < 1000:

    current_used_data = {
        "token": amount
    }

    current_used_trait = ""

    back_color = None
    face_color = None
    chin_color = None
    helmet_color = None

    armor_shape = None
    armor_color = None

    new_image = get_random_background_image()

    current_weight = 1

    done = True

    for idx, layer in enumerate(order):

        if layer == "Eyes":
            weight, layer_image_file = get_random_image(layer, excludes=[face_color])
        elif layer in ["Chin traits", "Helmet traits"]:
            weight, layer_image_file = get_random_image(layer, filter=back_color)
        elif layer == "Animal details":
            weight, layer_image_file = get_random_image(f"{armor_shape.title()} details" , excludes=[armor_color, back_color, chin_color, helmet_color])
        elif layer == "Armor":
            weight, layer_image_file = get_random_image(layer, excludes=[back_color, "moon" if back_color == "silver" else None, "silver" if back_color == "moon" else None])
        else:
            weight, layer_image_file = get_random_image(layer)

        if not layer_image_file:
            done = False
            break

        current_weight *= weight

        current_used_trait += layer_image_file

        layer_image = Image.open(layer_image_file)

        current_used_data[layer] = layer_image_file.split("/")[-1].split(".png")[0]

        if layer == "Back details":
            back_color = layer_image_file.split(".png")[0].split()[-1]
        elif layer == "Face details":
            face_color = layer_image_file.split(".png")[0].split()[-1]
        elif layer == "Chin traits":
            chin_color = layer_image_file.split(".png")[0].split()[-1]
        elif layer == "Helmet traits":
            helmet_color = layer_image_file.split(".png")[0].split()[-1]
        elif layer == "Armor":
            armor_shape = layer_image_file.split("/")[2].split()[1]
            armor_color = layer_image_file.split(".png")[0].split()[-1]

        new_image = Image.alpha_composite(new_image, layer_image)

    if done:

        if current_used_trait not in used_traits:

            used_traits.append(current_used_trait)

            used_data.append(current_used_data)

            newsize = (1050, 1050)
            new_image = new_image.resize(newsize, resample=Image.NEAREST)

            current_weight /= delimeter

            new_image.save(f"results/{current_weight:.20f}_{amount}.png")

            amount += 1

    i += 1
    print(i)

with open("results_data.json", "w") as tmp:
    json.dump(used_data, tmp, indent=4)
