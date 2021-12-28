#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple

FILE_DIR: Path = Path(__file__).parent.resolve()
HOST: str = "localhost"


# TODO: Choose a P value that is shared with the client.
P: int = 5


def calculate_shared_secret(x: int, y: int, z: int) -> int:
    # TODO: Calculate the shared secret and return it
    calculation = (x**y) % P
    return calculation


def exchange_base_number(sock: socket.socket) -> int:
    # TODO: Wait for a client message that sends a base number.
    proposal = int.from_bytes(sock.recv(4), 'big')
    # TODO: Return a message that the base number has been received.
    print("base number received: " + str(proposal))
    return proposal


def launch_server(server_port: int) -> Tuple[int, int, int]:
    # TODO: Create a server socket. can be UDP or TCP.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, server_port))
    sock.listen()
    client_sock, addr = sock.accept()
    # TODO: Wait for the client to propose a base for the key exchange.
    base = exchange_base_number(client_sock)
    print("Base int is %s" % base)
    # TODO: Wait for the nonce computed by the client.
    rx_int = int.from_bytes(client_sock.recv(4), 'big')
    # TODO: Also reply to the client.
    new_int = random.randint(1, 100)
    print("Int received from peer is %s" % rx_int)
    # TODO: Compute the shared secret using the secret number.
    shared_sec = (base**new_int)%P
    client_sock.send(shared_sec.to_bytes(4, 'big'))
    shared_secret = calculate_shared_secret(rx_int, new_int, P)
    print("Y is %s" % new_int)
    print("Shared secret is %s" % shared_secret)
    # TODO: Do not forget to close the socket.
    sock.close()
    # TODO: Return the base number, the secret integer, and the shared secret
    return base, new_int, shared_secret


def main(args):
    launch_server(args.server_port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--server-port",
        default="8000",
        type=int,
        help="The port the server will listen on.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
