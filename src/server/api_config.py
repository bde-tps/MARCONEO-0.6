"""
api_config.py

Defines the APIConfig class which is a dictionary
containing every json retrieved from the BDE API.
"""

#-------------------------------------------------------------------#

import sys
import decimal
import requests

#-------------------------------------------------------------------#

class APIJsons:
    """
    A dictionary containing every json retrieved from the BDE API.
    """
    def __init__(self, config_manager=None) -> None:
        super().__init__()
        self.config_manager = config_manager
        self.loggers = config_manager.app.loggers
        self.loggers.log.info("Retrieving API config...")
        self.config_json, self.categories_json = {}, {}

        self.setup_jsons()

        self.categories = self.retrieve_categories(self.categories_json)

        self.loggers.log.info("API configurations files retrieved.")

    def get_api(self, url) -> dict:
        """
        Retrieves the API config from the BDE API.
        """
        try:
            api_config_resp = requests.get(url,
                                      timeout=20)
            api_config_resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            self.loggers.log.error(err)
            print("Error with distant server, please try again later.")
            sys.exit(1)
        except requests.exceptions.ConnectionError as err:
            self.loggers.log.error(err)
            print("Can't reach distant server, please check your internet connection.")
            sys.exit(1)
        except requests.exceptions.Timeout as err:
            self.loggers.log.error(err)
            print("Timeout error, please check your internet connection.")
            sys.exit(1)
        return api_config_resp.json(parse_float=decimal.Decimal)

    def retrieve_categories(self, config) -> list:
        """
        Retrieves the categories from the API.
        """
        return [product_type["type"] for product_type in config]

    def setup_jsons(self) -> None:
        """
        Setup the jsons.
        """
        config = self.get_api("https://bde-pprd.its-tps.fr/api/product")
        self.config_manager.cat_selected_params(config)
        self.config_manager.cat_refill(config)
        self.config_manager.generate_json("config", config)
        self.config_json = config['data']

        config = self.get_api("https://bde-pprd.its-tps.fr/api/productType")
        self.config_manager.generate_json("categories", config)
        self.categories_json = config['data']
