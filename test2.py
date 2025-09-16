name_dict: dict = {
    "A": (1, 2, 3, 4),
    "B": (5, 6, 7, 8)
    }

import random


name_collection = random.choice(tuple(collection for collection in name_dict.values()))
print(name_collection)