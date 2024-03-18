import socket
import sys
import os


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
