import json
import os

class STAC_IO:
    """Methods used to read and save STAC json.
    Allows users of the library to set their own methods
    (e.g. for reading and writing from cloud storage)
    """
    @staticmethod
    def default_read_text_method(uri):
        with open(uri) as f:
            return f.read()

    @staticmethod
    def default_write_text_method(uri, txt):
        with open(uri, 'w') as f:
            f.write(txt)

    @staticmethod
    def default_stac_object_from_dict_method(d):
        if 'type' in d:
            return Item.from_dict(d)
        elif 'extent' in d:
            return Collection.from_dict(d)
        else:
            return Catalog.from_dict(d)

    read_text_method = default_read_text_method
    write_text_method = default_write_text_method

    # Replaced in __init__ to account for extension objects.
    stac_object_from_dict = default_stac_object_from_dict_method

    # This is set in __init__.py
    STAC_OBJECT_CLASSES = None

    @classmethod
    def read_text(cls, uri):
        return cls.read_text_method(uri)

    @classmethod
    def write_text(cls, uri, txt):
        cls.write_text_method(uri, txt)

    @classmethod
    def read_stac_json(cls, uri, root=None, parent=None):
        d = json.loads(STAC_IO.read_text(uri))
        return cls.stac_object_from_dict(d)

    @classmethod
    def save_json(cls, uri, json_dict):
        dirname = os.path.dirname(uri)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        STAC_IO.write_text(uri, json.dumps(json_dict, indent=4))
