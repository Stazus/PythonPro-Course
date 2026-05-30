# Reprezentacja żądania HTTP GET w Pythonie

http_get_request = {
    "start_line": {
        "method": "GET",           # pobranie danych
        "target": "/api/articles", # lista wszystkich artykułów
        "version": "HTTP/1.1"      # określa wersję protokołu HTTP używaną przez klienta i serwer
    },
    "headers": {
        "Host": "my-blog.com"      # domena serwera
    },
    "body": None                   # GET zwykle nie wysyła danych w ciele żądania
}

print(http_get_request)