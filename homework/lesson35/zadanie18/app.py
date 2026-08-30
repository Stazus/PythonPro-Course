import json


class ConfigManager:
    def __init__(self):
        self.config_json = """
        {
            "dev": {
                "region": "eu-central-1",
                "instance_type": "t3.micro",
                "db_size": "10 GB"
            },
            "staging": {
                "region": "eu-central-1",
                "instance_type": "t3.small",
                "db_size": "20 GB"
            },
            "production": {
                "region": "eu-west-1",
                "instance_type": "t3.medium",
                "db_size": "100 GB"
            }
        }
        """

        self.config = json.loads(self.config_json)

    def deploy(self, environment):
        if environment not in self.config:
            print(f"Nieznane środowisko: {environment}")
            return

        settings = self.config[environment]

        print(f"\nDeployment środowiska: {environment}")
        print(f"Region: {settings['region']}")
        print(f"Typ instancji EC2: {settings['instance_type']}")
        print(f"Rozmiar bazy danych: {settings['db_size']}")

    def compare(self, env1, env2):
        if env1 not in self.config or env2 not in self.config:
            print("Podano nieprawidłową nazwę środowiska.")
            return

        print(f"\nPorównanie: {env1} vs {env2}")

        config1 = self.config[env1]
        config2 = self.config[env2]

        for key in config1:
            value1 = config1[key]
            value2 = config2[key]

            if value1 != value2:
                print(
                    f"{key}: "
                    f"{env1}={value1}, "
                    f"{env2}={value2}"
                )
            else:
                print(f"{key}: bez różnic ({value1})")


if __name__ == "__main__":
    manager = ConfigManager()

    manager.deploy("dev")
    manager.deploy("staging")
    manager.deploy("production")

    manager.compare("dev", "production")
