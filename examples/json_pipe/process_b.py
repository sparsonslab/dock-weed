import json
import sys


def run(std_input):

    if not std_input:
        sys.stdout.write(json.dumps({
            "input": {"x": 1.0, "y": 1.0},
            "output": {"z": 1.0}
        }))
        return

    try:
        data = json.loads(std_input)
        print(json.dumps({
            "z": data['x'] + data['y']
        }))
    except (KeyError, json.decoder.JSONDecodeError):
        print(json.dumps({"error": "cannot parse input"}))


run(sys.stdin.readline())

