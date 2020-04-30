import json
import argparse
import os
from datetime import datetime
import pprint
import nesteddict
import sys


class GenerateName:
    
    def __init__(self, input_filename, ext):
        self._ext = ext
        self._version = ""
        self._input_filename, _ = os.path.splitext(input_filename)
        self._name = f"{self._input_filename}{self._ext}{self._version}"
        self._count = 0
        
    def name(self):
        if self._ext is None:
            return None
        if os.path.exists(self._name):
            self._count = self._count + 1
            self._version = f".{self._count}"
            self._name = f"{self._input_filename}{self._ext}{self._version}"
            return self.name()
        else:
            return self._name
        
    
def flatten_dict(d, prv_keys=[], sep="."):

    for k, v in d.items():
        if isinstance(v, dict):
            yield from flatten_dict(v, prv_keys + [k], sep)
        else:
            yield f"{sep.join(prv_keys + [k])}=\"{v}\""


def json_to_text(input_filename, output_filename=None, encoding="Latin-1", separator="."):
    with open(input_filename, "r", encoding=encoding) as input_file:
        input_dict = json.load(input_file)
        if output_filename:
            with open(output_filename, "w", encoding=encoding) as output_file:
                output_file.write(f"# Created '{output_filename}' at UTC: {datetime.utcnow()}\n")
                for line in flatten_dict(d=input_dict, prv_keys=[], sep=separator):
                    output_file.write(f"{line}\n")
        else:
            for line in flatten_dict(d=input_dict, prv_keys=[], sep=separator):
                print(line)


def text_to_json(input_filename, output_filename=None, encoding="Latin-1", separator="."):
    r = nesteddict.NestedDict()
    with open(input_filename, "r", encoding=encoding) as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            value = value.strip()
            r[key] = value.strip('"')

    if output_filename:
        with open(output_filename, "w", encoding=encoding) as output_file:
            output_file.write(json.dumps(r, indent=2))
            output_file.write("\n")
    else:
        print(json.dumps(r, indent=2))


def json_to_text_args(files, ext, encoding, separator):
    for f in files:
        namegen = GenerateName(f, ext)
        json_to_text(f, output_filename=namegen.name(), encoding=encoding, separator=separator)


def text_to_json_args(files, ext, encoding, separator):
    for f in files:
        namegen = GenerateName(f, ext)
        text_to_json(f, output_file=namegen.name(), encoding=encoding, separator=separator)

def iterate_args(files, output_filename, encoding, separator):
    for f in files:
        name, ext = os.path.splitext(f)
        if ext == ".json":
            json_to_text(f, output_filename=output_filename, encoding=encoding, separator=separator)
        elif ext == ".txt":
            decode_txt(f, output_filename=output_filename, encoding=encoding, separator=separator)
        else:
            print(f"Ignoring file: {f} unrecognised extension {ext}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--jsontotext', nargs='*')
    parser.add_argument('--texttojson', nargs='*')
    parser.add_argument('--separator', default=".",
                        help="Separator to use between JSON key names [default: %(default)s]")
    parser.add_argument('--encoding', default="Latin-1",
                        help="Encoding for read and write streams [default: %(default)s]")
    parser.add_argument('--ext', default=None,
                        help="send output to a corresponding file with this extension")
    args = parser.parse_args()

    output_file = None

    if args.texttojson and args.jsontotext:
        print("You cannot decode JSON and text files at the same time")
        sys.exit(1)

    if args.jsontotext:
        json_to_text_args(files=args.jsontotext,
                          ext=args.ext,
                          encoding=args.encoding,
                          separator=args.separator)

    if args.texttojson:
        text_to_json_args(files=args.texttojson,
                          ext=args.ext,
                          encoding=args.encoding,
                          separator=args.separator)


if __name__ == "__main__":
    main()
