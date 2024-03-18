import socket
import sys
import os


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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(2)

    option = sys.argv[1]
    if option == "-h":
        print_help()
        sys.exit(0)
    elif option == "-u":
        pass
    elif option == "-s":
        pass
    else:
        print("Invalid option")
        print_help()
        sys.exit(2)
