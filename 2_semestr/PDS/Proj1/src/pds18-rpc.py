import sys
import argparse

from tools import err_print

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', action="store", type=int,
        help="unique peer instance identifier, where you need to distinguish between them within a single guest")
    parser.add_argument('--peer', action="store_true",
        help="command for a peer instance")
    parser.add_argument('--node', action="store_true",
        help="command for a node instance")

    parser.add_argument('--command', action="store", type=str,
        choices=["message", "getlist", "peers", "reconnect", "database", "neighbors", "connect", "disconnect", "sync"],
        help="")

    #message
    parser.add_argument('--from', action="store", type=str,
        help="")
    parser.add_argument('--to', action="store", type=str,
        help="")
    parser.add_argument('--message', action="store", type=str,
        help="")

    #reconnect, connect
    parser.add_argument('--reg-ipv4', action="store", type=str,
        help="")
    parser.add_argument('--reg-port', action="store", type=int,
        help="")

    args = parser.parse_args()

    if args.peer == args.node:
       err_print("one of --peer and --node required")
       sys.exit(-1)

    return args

if __name__ == "__main__":
    args = get_args()
    print(args)