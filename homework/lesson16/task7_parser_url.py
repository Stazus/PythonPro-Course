def parse_url(url: str) -> dict:
    """Rozbiera adres URL na części."""

    protocol, remainder = url.split("://", 1)

    if "/" in remainder:
        host_part, path = remainder.split("/", 1)
        path = "/" + path
    else:
        host_part = remainder
        path = "/"

    if ":" in host_part:
        domain, port = host_part.split(":", 1)
        port = int(port)
    else:
        domain = host_part

        if protocol == "http":
            port = 80
        elif protocol == "https":
            port = 443
        else:
            port = None

    return {
        "protocol": protocol,
        "domain": domain,
        "port": port,
        "path": path
    }


url1 = "https://api.example.com:8080/users/search?active=true"
url2 = "https://my-blog.com/articles"
url3 = "http://example.com"

print(parse_url(url1))
print(parse_url(url2))
print(parse_url(url3))