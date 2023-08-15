"""
Module containing all the extensions used in the application
"""

import hashlib
import sys

from dotenv import dotenv_values

env_values = dotenv_values(".env")
required_variables = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_IP",
    "DB_NAME",
    "DB_TEST_NAME",
    "DB_PORT",
    "HASH_SALT",
    "SECRET_KEY",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
]


class SecurityManager:
    """
    Class containing security related methods
    """

    @staticmethod
    def validate_env():
        """
        Function to validate the .env file
        """
        missing_variables = [var for var in required_variables if var not in env_values]

        if missing_variables:
            missing = list(missing_variables)
            print(f"ERROR: .env variables missing: {missing}")
            sys.exit(1)

    @staticmethod
    def hash(hash_string: str):
        """Function to hash a string

        Args:
            hash_string (str): String to be hashed

        Returns:
            str: Hashed string
        """ """"""
        return hashlib.md5(
            str(hash_string + env_values["HASH_SALT"]).encode()
        ).hexdigest()

    @staticmethod
    def compare_hash(hashed_string: str, hash_string: str):
        """Function to compare a hashed string with a string

        Args:
            hashed_string (str): Hashed string
            hash_string (str): String to be hashed

        Returns:
            bool: True if the strings match, False otherwise
        """
        if hashed_string == SecurityManager.hash(hash_string):
            return True
        return False
