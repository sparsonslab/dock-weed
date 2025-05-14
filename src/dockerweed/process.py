# Copyright (c) 2025-2025. Dr Sean Paul Parsons. All rights reserved.
from abc import abstractmethod
import json
import random
import subprocess


class NodeProcess:
    """ A node's process, the code a node runs/executes.

    Attributes
    ----------
    name: str
        The name of the process.
    description: str
        A brief description of the process.
    inputs: dict
        A flat dictionary of input variables to the process.
    outputs: dict
        A flat dictionary of output variables of the process.
    """
    def __init__(
            self,
            name: str,
            description: str,
            inputs: dict,
            outputs: dict
    ):
        self.name = name
        self.description = description
        self.inputs = inputs
        self.outputs = outputs

    @abstractmethod
    def run(self, inputs: dict) -> dict:
        """ Run the process.

        Arguments
        ---------
        inputs: dict
            A flat dictionary of input variables to the process, with keys
            matching self.inputs.
        """
        pass


class ContainerProcess(NodeProcess):
    """ A node process consisting of a Docker container.

    Attributes
    ----------
    container: str
        The name of the container.
    command: str
        The command to the container that the node runs.
        This will be the value of one of the container image's labels. The
        label's key will be self.name.
    """
    def __init__(
            self,
            name: str,
            description: str,
            inputs: dict,
            outputs: dict,
            container: str,
            command: str,
    ):
        self.container = container
        self.command = command
        super().__init__(
            name=name,
            description=description,
            inputs=inputs,
            outputs=outputs
        )

    def run(self, inputs: dict) -> dict:
        # Check inputs
        # ???????

        # Pipe the inputs into the node's command.
        cmd = f"echo '{json.dumps(inputs)}' | docker exec -i {self.container} {self.command}"
        result = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        # Get the output JSON.
        try:
            return json.loads(result.stdout)
        except json.decoder.JSONDecodeError:
            return {}


class UniformFloatProcess(NodeProcess):
    """ A process that generates uniformly distributed floats. """
    def __init__(self):
        super().__init__(
            name="random float",
            description=f"A uniformly distributed random float.",
            inputs={"min": 0.0, "max": 1.0},
            outputs={"n": 0.5}
        )

    def run(self, inputs: dict) -> dict:
        return {"n": random.uniform(inputs["min"], inputs["max"])}


class RandomChoice(NodeProcess):
    """ A process that picks randomly from a set. """
    def __init__(self):
        super().__init__(
            name="random choice",
            description=f"A rnadom choice.",
            inputs={"choices": [1, 2, 3, 4]},
            outputs={"choice": 1}
        )

    def run(self, inputs: dict) -> dict:
        return {"choice": random.choice(inputs["choices"])}
