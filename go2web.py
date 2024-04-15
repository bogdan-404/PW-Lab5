#!/usr/bin/env python3
import socket
import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import ssl


def send_request(host, port, path, use_https=False):
    request_line = f"GET {path} HTTP/1.1\r\n"
    headers = f"Host: {host}\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nConnection: close\r\n\r\n"
    response_data = b""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if use_https:
            context = ssl.create_default_context()
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.connect((host, port))
                ssock.sendall((request_line + headers).encode())
                while True:
                    chunk = ssock.recv(4096)
                    if not chunk:
                        break
                    response_data += chunk
        else:
            sock.connect((host, port))
            sock.sendall((request_line + headers).encode())
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
    return response_data


def fetch_url(url, limit=5):
    if limit == 0:
        print("Exceeded redirect limit")
        return

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme or "http"
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else "/"
    if parsed_url.query:
        path += "?" + parsed_url.query
    use_https = scheme == "https"
    port = 443 if use_https else 80

    response = send_request(host, port, path, use_https=use_https)
    header, _, body = response.partition(b"\r\n\r\n")

    if b"400 Bad Request" in header:
        print("400 Bad Request")
        print(header.decode())
        return

    headers = header.decode().split("\r\n")
    for h in headers:
        if "Location" in h:
            location = h.split(": ")[1].strip()
            if not urlparse(location).netloc:
                location = f"{scheme}://{host}{location}"
            print(f"Redirecting to {location}")
            fetch_url(location, limit - 1)
            return

    soup = BeautifulSoup(body, "html.parser")
    print(soup.get_text())


def print_help():
    help_text = """Usage: go2web [OPTION]... [ARGUMENT]...
    -u <URL>         make an HTTP request to the specified URL and print the response
    -s <search-term> make an HTTP request to search the term using your favorite search engine and print top 10 results
    -h               show this help
    """
    print(help_text)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(2)

    option = sys.argv[1]
    if option == "-h":
        print_help()
        sys.exit(0)
    elif option == "-u":
        fetch_url(sys.argv[2])
    elif option == "-s":
        pass
    else:
        print("Invalid option")
        print_help()
        sys.exit(2)
