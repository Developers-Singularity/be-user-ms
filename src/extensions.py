import hashlib

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
        missing_variables = [var for var in required_variables if var not in env_values]

        if missing_variables:
            missing = ",".join([key for key in missing_variables])
            print(f"ERROR: .env variables missing: {missing}")
            exit(0)

    @staticmethod
    def hash(hash_string: str):
        return hashlib.md5(
            str(hash_string + env_values["HASH_SALT"]).encode()
        ).hexdigest()

    @staticmethod
    def compare_hash(hashed_string: str, hash_string: str):
        if hashed_string == SecurityManager.hash(hash_string):
            return True
        return False
