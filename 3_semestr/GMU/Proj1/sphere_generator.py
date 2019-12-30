# @file sphere_generator.py
# @author Václav Martinka a Petr Buchal
# @date 29. 12. 2019 (15:41)


import argparse
import random as ran


parser = argparse.ArgumentParser()
parser.add_argument("--count", "-c", action="store", type=int, required=True)
parser.add_argument("--start", "-s", action="store", type=float, default=0.0)
parser.add_argument("--end", "-e", action="store", type=float, default=1000.0)
parser.add_argument("--maximal_size", "-m", action="store", type=float, default=100.0)

args = parser.parse_args()


for i in range(args.count):
	print(ran.uniform(args.start, args.end), ran.uniform(args.start, args.end), ran.uniform(args.start, args.end), ran.uniform(0, args.maximal_size))
