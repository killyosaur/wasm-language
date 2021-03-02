import argparse
from Emitter.emitter import Emitter
from Tokenizer.tokens import Tokenize
from Parser.parse import Parser

def Compile(src: str):
    tokens = Tokenize(src)
    ast = Parser(tokens).parser()
    wasm = Emitter(ast)
    f = open("output.wasm", "w")
    for x in wasm:
        f.write(str(x))
    f.close()

parser = argparse.ArgumentParser()
parser.add_argument("source")
args = parser.parse_args()
Compile(args.source)
