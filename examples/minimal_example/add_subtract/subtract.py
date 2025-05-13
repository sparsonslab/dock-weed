import json
import sys


def main():

    try:
        data = json.loads(sys.stdin.readline())
        sys.stdout.write(json.dumps({
            "z": data['x'] - data['y']
        }))
        return 0
    except (json.decoder.JSONDecodeError, KeyError):
        pass

    # Provide data about this node.
    sys.stdout.write(json.dumps({
        "description": "Addition. z = x + y.",
        "inputs": {"x": 1.0, "y": 1.0},
        "outputs": {"z": 1.0}
    }))
    return 0


if __name__ == '__main__':
    sys.exit(main())
