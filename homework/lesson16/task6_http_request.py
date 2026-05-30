class HttpRequest:
    """Reprezentuje żądanie HTTP."""

    def __init__(self, method, target, headers=None, body=None):
        self.method = method
        self.target = target
        self.headers = headers if headers is not None else {}
        self.body = body

    def display(self):
        """Wyświetla żądanie HTTP w czytelnej formie."""

        print("--- HTTP Request ---")

        print(f"Method: {self.method}")
        print(f"Target: {self.target}")

        print("Headers:")

        for key, value in self.headers.items():
            print(f" {key}: {value}")

        print("Body:")

        if self.body:
            print(self.body)
        else:
            print("(empty)")

        print("--------------------")


request = HttpRequest(
    method="POST",
    target="/api/articles",
    headers={
        "Host": "my-blog.com",
        "User-Agent": "PythonClient/1.0"
    },
    body='{"title": "Nowy artykul"}'
)

request.display()