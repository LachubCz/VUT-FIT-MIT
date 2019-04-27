import argparse

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', action="store", type=int,
        help="unique peer instance identifier, where you need to distinguish between them within a single guest")
    parser.add_argument('--reg-ipv4', action="store", type=str,
        help="IP address to which the peer will regularly send HELLO messages and GETLIST queries")
    parser.add_argument('--reg-port', action="store", type=int,
        help="registration node port to which the peer will regularly send HELLO messages and GETLIST queries")

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    pass