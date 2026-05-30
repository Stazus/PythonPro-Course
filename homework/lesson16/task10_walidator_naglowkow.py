def validate_request(request_dict: dict):
    """Sprawdza obecność wymaganych nagłówków HTTP."""

    headers = request_dict.get("headers", {})

    if "Host" not in headers:
        raise ValueError("Brak wymaganego nagłówka: Host")

    if "User-Agent" not in headers:
        raise ValueError("Brak wymaganego nagłówka: User-Agent")

    print("Żądanie jest poprawne.")


# Poprawne żądanie

correct_request = {
    "headers": {
        "Host": "my-blog.com",
        "User-Agent": "PythonClient/1.0"
    }
}

# Niepoprawne żądanie - brak User-Agent

incorrect_request = {
    "headers": {
        "Host": "my-blog.com"
    }
}


print("Test poprawnego żądania:")

try:
    validate_request(correct_request)

except ValueError as e:
    print(e)


print("\nTest niepoprawnego żądania:")

try:
    validate_request(incorrect_request)

except ValueError as e:
    print(e)