class FakeServer:
    """Prosta symulacja serwera."""

    def __init__(self):
        self.db = {
            "users": [
                {"id": 1, "name": "Jan"},
                {"id": 2, "name": "Anna"}
            ]
        }

    def handle_request(self, request: dict) -> dict:
        """Obsługuje żądanie klienta."""

        method = request.get("method")
        target = request.get("target")
        body = request.get("body")

        if method == "GET" and target == "/users":
            return {
                "status_code": 200,
                "message": "OK",
                "body": self.db["users"]
            }

        elif method == "POST" and target == "/users":
            new_id = len(self.db["users"]) + 1

            new_user = {
                "id": new_id,
                "name": body["name"]
            }

            self.db["users"].append(new_user)

            return {
                "status_code": 201,
                "message": "Created",
                "body": new_user
            }

        else:
            return {
                "status_code": 404,
                "message": "Not Found",
                "body": None
            }


class FakeClient:
    """Prosta symulacja klienta."""

    def send(self, server: FakeServer, request: dict):
        """Wysyła żądanie do serwera i drukuje odpowiedź."""

        print("\n--- Request ---")
        print(request)

        response = server.handle_request(request)

        print("--- Response ---")
        print(response)


server = FakeServer()
client = FakeClient()

# 1. Pobranie wszystkich użytkowników
get_users_request = {
    "method": "GET",
    "target": "/users",
    "body": None
}

client.send(server, get_users_request)

# 2. Dodanie nowego użytkownika
post_user_request = {
    "method": "POST",
    "target": "/users",
    "body": {
        "name": "Katarzyna"
    }
}

client.send(server, post_user_request)

# 3. Ponowne pobranie użytkowników po dodaniu nowego
client.send(server, get_users_request)

# 4. Próba dostępu do nieistniejącego zasobu
wrong_request = {
    "method": "GET",
    "target": "/products",
    "body": None
}

client.send(server, wrong_request)