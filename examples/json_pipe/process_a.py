import json
import sys


output_data = {
    "name": "a funny script",
    "x": 67.98769,
    "y": 56.78,
    "z": 32
}

json.dump(output_data, sys.stdout)

