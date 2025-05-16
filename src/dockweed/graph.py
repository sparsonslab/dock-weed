from typing import List

from .process import NodeProcess
from .topological_sort import kahns_algorithm


class Graph:
    """ A graph of processes.

    Parameters
    ----------
    specification: dict
        Specifies the structure of the graph.
        For each node in the graph (key in the specification), a specification
        of the process to be run and the process's inputs:
        {<node name>: {"process": <NodeProcess.name>, "inputs": {<variable>:<value>, ...}}, ...}
        Inputs from other nodes (i.e. incoming edges) are specified by a tuple:
        <input variable>: (<other node name>, <other node output variable>)
    processes: [NodeProcess]
        All processes available.

    Raises
    ------
    KeyError
        The specification is not formatted correctly (missing keys, etc.).
        A named process is not available.
        Specified inputs do not match those of the process (variable name or type).
    Exception
        The graph is cyclic.

    Attributes
    ----------
    specification: dict
        As for specification parameter.
    processes: {<node name>: NodeProcess}
        The processes of every node in the graph.
    topology: dict
        The incoming node edges of every node in the graph.
    node_order: [str]
        The node names in order of execution.
    """
    def __init__(self, specification: dict, processes: List[NodeProcess]):

        # Check specification and processes.
        errors = []
        self.specification = {}
        self.processes = {}
        for node, spec in specification.items():

            # Process.
            if "process" not in spec:
                errors.append(f"Node {node}: No process is specified.")
                continue
            process_name = spec["process"]
            node_process = [process for process in processes if process.name == process_name]
            if not node_process:
                errors.append \
                    (f"Node {node}: There is no process named {process_name}.")
                continue
            self.processes[node] = node_process[0]

            # Inputs.
            if "inputs" not in spec:
                errors.append(f"Node {node}: No inputs are specified.")
                continue
            process_variables = set(self.processes[node].inputs.keys())
            spec_variables = set(spec["inputs"].keys())
            if process_variables != spec_variables:
                errors.append \
                    (f"Node {node}: The specified inputs do not match the process inputs.")
                continue
            self.specification[node] = spec

            # todo - check input types against processes.

        if errors:
            raise KeyError("\n".join(errors))

        # Topology (edges).
        self.topology = {}
        for node, specification in self.specification.items():
            self.topology[node] = [
                value[0]
                for name, value in specification["inputs"].items()
                if isinstance(value, tuple) and len(value) == 2
            ]

        # Topological order.
        self.node_order = kahns_algorithm(self.topology, incoming=True)
        if not self.node_order:
            raise Exception("The graph is cyclic!")

    def is_input(self, node: str, variable: str) -> bool:
        """ Does the graph have a node with the given input variable? """
        return node in self.processes and variable in self.processes[node].inputs

    def input_value(self, node: str, variable: str):
        """ Get the value of the given input variable of the given node. """
        if self.is_input(node, variable):
            return self.specification[node]["inputs"][variable]
        return None

    def input_is_egde(self, node: str, variable: str) -> bool:
        """ Is the node variable an edge?"""
        return isinstance(self.input_value(node, variable), tuple)

    def is_output(self, node: str, variable: str) -> bool:
        """ Does the graph have a node with the given output variable? """
        return node in self.processes and variable in self.processes[node].outputs

    def output_value(self, node: str, variable: str):
        """ Get the (default) value of the given output variable of the given node. """
        if self.is_output(node, variable):
            return self.processes[node].outputs[variable]
        return None

    def run(self):
        """ Execute the graph.

        Returns
        -------
        inputs: dict
            The graph inputs.
            {<node name>: {<variable>:<value>, ...}, ...}
        outputs: dict
            The graph outputs.
            {<node name>: {<variable>:<value>, ...}, ...}
        """
        inputs = {}
        outputs = {}
        for node in self.topology:
            # Substitute tuple inputs with outputs from prior nodes.
            inputs[node] = self.specification[node]["inputs"].copy()
            for input_name, value in inputs[node].items():
                if not isinstance(value, tuple):
                    continue
                try:
                    incoming_node, incoming_variable = value
                    incoming_value = outputs[incoming_node][incoming_variable]
                    inputs[node][input_name] = incoming_value
                except KeyError:
                    raise KeyError(f"Invalid inputs for")

            # Execute, storing the outputs.
            outputs[node] = self.processes[node].run(inputs[node])

        return inputs, outputs
