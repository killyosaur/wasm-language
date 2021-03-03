import argparse
from emitter import Emitter
from tokenParser import Parse
from tokenizer import Tokenize

def compile(src: str):
    tokens = Tokenize(src)
    ast = Parse(tokens)
    wasm = Emitter(ast)
    
    f = open("output.wasm", "wb")
    f.write(wasm)
    f.close()

argParser = argparse.ArgumentParser()
argParser.add_argument("source")
args = argParser.parse_args()
compile(args.source)
