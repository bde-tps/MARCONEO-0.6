"""
config.py

Contains the config class.
Contains the config class which is
used to store the configuration data
of the application.
"""

#-------------------------------------------------------------------#

import json
import os
import decimal

from src.server.api_config import APIJsons

#-------------------------------------------------------------------#

class Config:
    """
    Stores the configuration data of the application.
    """
    DEFAULT = "default"
    CUSTOM = "config"
    def __init__(self, app) -> None:
        """
        Reads the json file (./config.json).
        Shuts down the process if an error occurs.

        The json file is used to configure the images and the shopping menus
        (items, prices, etc.)
        """
        self.loggers = app.loggers
        self.app = app

        self.api_config = APIJsons(self)
        self.loaded_config = {}

        # By default, the config is set to default.
        self.name = self.DEFAULT
        self.default_config = self.load(self.DEFAULT)

    def generate_json(self, name, json_retrieved:json) -> bool:
        """
        Generate a json file corresponding
        to the request response given.
        """

        with open(os.path.join(os.getcwd(),"data","json", f"{name}.json"),
                  'w',
                  encoding="utf-8") as file:
            file.write(json.dumps(json_retrieved, indent=4))

    def load(self, file_name:str=None) -> dict:
        """
        Loads the json file onto loaded_config and copies it to initial_config.
        Returns a dictionary containing the json file data.
        """
        if file_name is None:
            return {}
        dictionary = {}

        with open(os.path.join(os.getcwd(),"data","json", f"{file_name}.json"),
                  'r',
                  encoding="utf-8") as file:
            json_content = file.read()
        try:
            dictionary.update(json.loads(json_content, parse_float=decimal.Decimal))
        except json.JSONDecodeError as decode_err:
            self.loggers.log.warning("Error while parsing the config.json file at line %s",
                                     decode_err.lineno)
            self.app.close()
        return dictionary["data"]

    def update_custom_config(self, new_config:dict) -> None:
        """
        Updates the custom config.
        """
        self.api_config.config_json = new_config

    def update_loaded_config(self) -> None:
        """
        Updates the loaded config.
        """
        match self.name:
            case self.DEFAULT:
                self.loaded_config = self.default_config
            case self.CUSTOM:
                self.loaded_config = self.api_config.config_json

    def change_price(self, toggle, item_name, new_price):
        """
        Changes the price of an item.
        """
        for product_type in self.loaded_config:
            if product_type["product_type"] == toggle:
                for item in product_type["products"]:
                    if item['title'] == item_name:
                        item['price'] = decimal.Decimal(new_price)
                        break

    def cat_refill(self, config) -> None:
        """
        Concatenates the refill toggle to the loaded json.
        """
        with open(os.path.join(os.getcwd(),"data","json", "refill.json"),
                  'r',
                  encoding="utf-8") as file:
            refill_content = file.read()

        refill_dict = json.loads(refill_content, parse_float=decimal.Decimal)
        config['data'].append(refill_dict['refill'])

    def get_custom_categories(self) -> list:
        """
        Returns the categories of the loaded config.
        """
        return [product_type["product_type"] for product_type in self.api_config.config_json
                 if any(product["selected"] for product in product_type["products"])]

    def get_product_types(self) -> list:
        """
        Returns the categories of the default config.
        """
        match self.name:
            case self.DEFAULT:
                return [product_type["product_type"] for product_type in self.default_config]
            case self.CUSTOM:
                return self.get_custom_categories()

    def cat_selected_params(self, config) -> list:
        """
        Add the selected bool parameter to the custom config
        """
        for items in config['data']:
            for product in items["products"]:
                product["selected"] = False
