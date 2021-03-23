import argparse
from processors import emitter, parser, tokenizer, transformer

def compile(src: str, out: str):
  tokens = tokenizer.Tokenize(src)
  ast = parser.Parse(tokens)
  transformedAst = transformer.Transform(ast)
  wasm = emitter.Emit(transformedAst)

  f = open(out, 'wb')
  f.write(wasm)
  f.close()

argParser = argparse.ArgumentParser(description='Python rewrite of the Chasm WASM compiler')
argParser.add_argument('source', metavar='src', type=str,
                       nargs=1, help='the source code for the application')
argParser.add_argument('-o', dest='output', type=str, nargs=1, default=['output'], help='the output file name (default "output"), will add the extension for you')
args = argParser.parse_args()

compile(args.source[0], f'{args.output[0]}.wasm')