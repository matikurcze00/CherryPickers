import yaml
from typing import Optional


class Confing:

    def __init__(self):
        self.ip_address: Optional[str] = None
        self.port: Optional[str] = None

    def load_config(self, path_to_config: str):
        with open(path_to_config) as f:
            config_d = yaml.safe_load(f)
            api_conf = config_d["api"]
            self.port = api_conf.get("port") or None
            self.ip_address = api_conf.get("ip_address") or None


cf = Confing()
