import json
import sys


def run(std_input):

    if not std_input:
        sys.stdout.write(json.dumps({
            "input": {"a": 1.0, "b": 1.0},
            "output": {"beta": 1.0}
        }))
        return

    try:
        data = json.loads(std_input)
        print(json.dumps({
            "beta": data['a'] * data['b']
        }))
    except (KeyError, json.decoder.JSONDecodeError):
        print(json.dumps({"error": "cannot parse input"}))


run(sys.stdin.readline())
