import yaml
from typing import Optional


class Confing:

    def __init__(self):
        self.ip_address: Optional[str] = None
        self.port: Optional[str] = None
        self.redis: Optional[dict] = None

    def load_config(self, path_to_config: str):
        with open(path_to_config) as f:
            config_d = yaml.safe_load(f)
            api_conf = config_d["api"]
            self.port = api_conf.get("port") or None
            self.ip_address = api_conf.get("ip_address") or None
            self.redis = config_d["redis"]


class ConfingAlgo:
    def __init__(self):
        self.receiver: Optional[dict] = None
        self.sender: Optional[dict] = None
        self.service_type: Optional[str] = None
        self.pdf_parameters: Optional[dict] = None

    def load_config(self, path_to_config: str):
        with open(path_to_config) as f:
            config_alg = yaml.safe_load(f)
            self.receiver = config_alg["receiver"]
            self.sender = config_alg["sender"]
            self.service_type = config_alg["service_type"]
            self.pdf_parameters = config_alg["pdf_parameters"]

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "service_type": self.service_type,
            "pdf_parameters": self.pdf_parameters
        }

    def update(self, config_dict: dict):
        self.receiver = config_dict["receiver"]
        self.sender = config_dict["sender"]
        self.service_type = config_dict["service_type"]
        self.pdf_parameters = config_dict["pdf_parameters"]


cf = Confing()
cf_algo = ConfingAlgo()

if __name__ == '__main__':
    conf_algo = ConfingAlgo()
    conf_algo.load_config("config_app.yaml")
