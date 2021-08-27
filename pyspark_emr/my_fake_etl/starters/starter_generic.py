import importlib
import sys

uri = sys.argv[1]

module = importlib.import_module(uri)
module.main()
