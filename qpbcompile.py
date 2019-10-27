import os
import time
import argparse
import compiler

parser = argparse.ArgumentParser(description='Convert .led file to PICBASIC.')
parser.add_argument('-a', '--all', help = 'compile all input files in the same directory as this script.',action="store_true")
parser.add_argument('-s', help = 'compile a specific file with a specified path.')
args = parser.parse_args()


if args.s:
    prevTime = time.time()
    compiler.compile_file(args.s)
    print("Compiled " + args.s + " in", round(time.time() - prevTime, 3), "seconds")

if args.all:
    led_files = [i for i in os.listdir() if i[-4:] == ".led"]
    for input_file in led_files:
        prevTime = time.time()
        compiler.compile_file(input_file)
        print("Compiled " + input_file + " in", round(time.time() - prevTime, 3), "seconds")
