import os

from pydantic import BaseModel, SecretStr


class TrubricsDefaults(BaseModel):
    # no stress, this is not a secret api key
    firebase_api_key: str = "AIzaSyAWGOaN7_sL98irVM2g5O2RULK4yj9Tdvs"
    firebase_project_id: str = "trubrics-ea-prod"
    trubrics_url: str = "https://ea.trubrics.com/"
    demo_sign_up_url: str = "https://trubrics.com/demo/"


class TrubricsConfig(BaseModel):
    firebase_auth_api_url: str
    firestore_api_url: str
    username: str
    email: str
    password: SecretStr
    project: str

    class Config:
        json_encoders = {SecretStr: lambda v: v.get_secret_value() if v else None}

    def save(self):
        config_path = os.path.join(os.path.expanduser("~"), ".trubrics_config.json")
        with open(config_path, "w") as file:
            file.write(self.json(indent=4))


def load_trubrics_config() -> TrubricsConfig:
    config_path = os.path.join(os.path.expanduser("~"), ".trubrics_config.json")
    if os.path.exists(config_path):
        return TrubricsConfig.parse_file(config_path)
    else:
        raise FileNotFoundError("Trubrics config file not found. Run `trubrics init` to generate this file.")
