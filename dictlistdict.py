import json
import argparse
import os
from datetime import datetime
import pprint
import nesteddict
import sys


def flatten_dict(d, prv_keys=[], sep="."):

    for k, v in d.items():
        if isinstance(v, dict):
            yield from flatten_dict(v, prv_keys + [k], sep)
        else:
            yield f"{sep.join(prv_keys + [k])}=\"{v}\""


def decode_json(input_filename, output_file, encoding, separator="."):
    with open(input_filename, "r", encoding=encoding) as input_file:
        input_dict = json.load(input_file)
        if output_file:
            for line in flatten_dict(d=input_dict, prv_keys=[], sep=separator):
                output_file.write(f"{line}\n")
        else:
            for line in flatten_dict(d=input_dict, prv_keys=[], sep=separator):
                print(line)


def decode_text(input_filename, output_file, encoding, separator="."):
    r = nesteddict.NestedDict()
    with open(input_filename, "r", encoding=encoding) as input_file:
        for line in input_file.readlines():
            key, _, value = line.partition("=")
            value = value.strip()
            r[key] = value.strip('"')

    if output_file:
        output_file.write(json.dumps(r, indent=2))
        output_file.write("\n")
    else:
        print(json.dumps(r, indent=2))



def decode_json_args(files, output_file, encoding, separator):
    for f in files:
        decode_json(f, output_file=output_file, encoding=encoding, separator=separator)


def decode_text_args(files, output_file, encoding, separator):
    for f in files:
        decode_text(f, output_file=output_file, encoding=encoding, separator=separator)

def iterate_args(files, output_file, encoding, separator):
    for f in files:
        name, ext = os.path.splitext(f)
        if ext == ".json":
            decode_json(f, output_file=output_file, encoding=encoding, separator=separator)
        elif ext == ".txt":
            decode_txt(f, output_file=output_file, encoding=encoding, separator=separator)
        else:
            print(f"Ignoring file: {f} unrecognised extension {ext}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--decodejson', nargs='*')
    parser.add_argument('--decodetext', nargs='*')
    parser.add_argument('--separator', default=".",
                        help="Separator to use between JSON key names [default: %(default)s]")
    parser.add_argument('--encoding', default="Latin-1",
                        help="Encoding for read and write streams [default: %(default)s]")
    parser.add_argument('--output', default=None,
                        help="send output to a corresponding file of the same name")
    args = parser.parse_args()

    output_file = None

    if args.decodejson and args.decodetext:
        print("You cannot decode JSON and text files at the same time")
        sys.exit(1)

    if args.output:
        output_file = open(args.output, "w", encoding=args.encoding)

    if args.decodejson:
        decode_json_args(files=args.decodejson,
                         output_file=output_file,
                         encoding=args.encoding,
                         separator=args.separator)

    if args.decodetext:
        decode_text_args(files=args.decodetext,
                         output_file=output_file,
                         encoding=args.encoding,
                         separator=args.separator)

    if output_file:
        print(f"Output written to {args.output}")

if __name__ == "__main__":
    main()
