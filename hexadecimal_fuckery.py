import os
import argparse

parser = argparse.ArgumentParser(description="quickly make ur MP4s really long!")
parser.add_argument("-i", metavar="mp4", type=str, required=True,
                    help="the input file")
parser.add_argument("-o", metavar="output", type=str, required=False,
                    help="the patched mp4 that will be created (default \"<filename>-long.mp4\")")
args = parser.parse_args()
assert(os.path.isfile(args.i))  # if you're seeing this, you gave me a file that doesnt exist :(
assert(args.i.endswith(".mp4"))  # if you're seeing this, you should know that this only works on MP4s

if not args.o:
    args.o = args.i.replace(".mp4", "-long.mp4")  # totally error-free.. right?

with open(args.i, "rb") as f:
    data = bytearray(f.read())
mvhd = data.index(b"mvhd")  # according to the mp4 specification, "mvhd" + 16 bits after is the vid length

# this will change the vid length to the largest 32-bit integer in hexadecimal, 0x7FFFFFFF (2,147,483,647)
data[mvhd + 20] = 127
for i in (21, 22, 23):
    data[mvhd + i] = 255

# and this changes the uh.. well, idrk, but it makes the vid longer!
for i in (16, 17, 18):
    data[mvhd + i] = 0
data[mvhd + 19] = 1

with open(args.o, "wb") as f:
    f.write(data)
print(f"[*] saved to {args.o}!")
