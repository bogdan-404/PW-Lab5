#!/usr/bin/env python3
import socket
import sys
import os
from urllib.parse import urlparse, quote_plus
from bs4 import BeautifulSoup


def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request)
        response = s.recv(4096)
        while len(response) > 0:
            print(response.decode("utf-8", "ignore"), end="")
            response = s.recv(4096)


def print_help():
    help_text = """Usage: go2web [OPTION]... [ARGUMENT]...
    -u <URL>         make an HTTP request to the specified URL and print the response
    -s <search-term> make an HTTP request to search the term using your favorite search engine and print top 10 results
    -h               show this help
    """
    print(help_text)


def fetch_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path if parsed_url.path != "" else "/"
    request_line = f"GET {path} HTTP/1.1\r\n"
    headers = f"Host: {parsed_url.netloc}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n"
    response = send_request(parsed_url.netloc, 80, (request_line + headers).encode())
    soup = BeautifulSoup(response, "html.parser")
    print(soup.get_text())


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
