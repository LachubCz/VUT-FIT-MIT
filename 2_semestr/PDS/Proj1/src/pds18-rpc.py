import os
import sys
import argparse

from tools import err_print, get_pipe_name

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', action="store", type=int, required=True,
        help="unique peer instance identifier, where you need to distinguish between them within a single guest")
    parser.add_argument('--peer', action="store_true",
        help="command for a peer instance")
    parser.add_argument('--node', action="store_true",
        help="command for a node instance")

    parser.add_argument('--command', action="store", type=str, required=True,
        choices=["message", "getlist", "peers", "reconnect", "database", "neighbors", "connect", "disconnect", "sync"],
        help="")

    parser.add_argument('--from', action="store", type=str, dest="from_",
        help="")
    parser.add_argument('--to', action="store", type=str,
        help="")
    parser.add_argument('--message', action="store", type=str,
        help="")

    parser.add_argument('--reg-ipv4', action="store", type=str,
        help="")
    parser.add_argument('--reg-port', action="store", type=int,
        help="")

    args = parser.parse_args()

    if args.peer == args.node:
        err_print("one of --peer and --node required")
        sys.exit(-1)

    if args.command == "message":
        if args.from_ == None or args.to == None or args.message == None:
            err_print("--from --to and --message are required for this command")
            sys.exit(-1)
    elif args.command == "reconnect" or args.command == "connect":
        if args.reg_ipv4 == None or reg_port == None:
            err_print("--reg-ipv4 and --reg-port are required for this command")
            sys.exit(-1)

    if args.peer:
        if args.command == "database" or args.command == "neighbors" or args.command == "connect" or args.command == "disconnect" or args.command == "sync":
            err_print("wrong combination of command and peer/node")
            sys.exit(-1)
    elif args.node:
        if args.command == "message" or args.command == "getlist" or args.command == "peers" or args.command == "reconnect":
            err_print("wrong combination of command and peer/node")
            sys.exit(-1)

    return args


if __name__ == "__main__":
    args = get_args()

    if args.peer:
        path = get_pipe_name("peer", args.id)
    elif args.node:
        path = get_pipe_name("node", args.id)

    pipe = open(path, "w")

    if args.command == "message":
        pipe.write("{} {} {} {}" .format(args.command, args.from_, args.to, args.message))
    elif args.command == "getlist":
        pipe.write("{}" .format(args.command))
    elif args.command == "peers":
        pipe.write("{}" .format(args.command))
    elif args.command == "reconnect":
        pipe.write("{} {} {}" .format(args.command, args.reg_ipv4, args.reg_port))
    elif args.command == "database":
        pipe.write("{}" .format(args.command))
    elif args.command == "neighbors":
        pipe.write("{}" .format(args.command))
    elif args.command == "connect":
        pipe.write("{} {} {}" .format(args.command, args.reg_ipv4, args.reg_port))
    elif args.command == "disconnect":
        pipe.write("{}" .format(args.command))
    elif args.command == "sync":
        pipe.write("{}" .format(args.command))

    pipe.close()
    os.remove(path)
