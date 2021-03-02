import argparse
from emitter import emitter

def compile():
    wasm = emitter()
    f = open("output.wasm", "wb")
    f.write(wasm)
    f.close()

parser = argparse.ArgumentParser()
compile()
