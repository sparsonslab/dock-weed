# Copyright (c) 2025-2025. Dr Sean Paul Parsons. All rights reserved.
import subprocess


class NodeContainer:
    """ A node's docker container.

    Attributes
    ----------
    image: str
        The image "name:tag".
    name: str
        The container name.
        The container will only actually exist after calling self.start().
    """
    def __init__(self, image_tag):
        self.image = image_tag
        self.name = image_tag.split(":")[0]

    def start(self):
        """ Start the container in detached mode. """
        cmd = f"docker run --name {self.name} -i -d {self.image}"
        _ = subprocess.run(cmd, shell=True)

    def stop(self):
        """ Stop the container and remove it. """
        cmd = f"docker rm {self.name} -f"
        _ = subprocess.run(cmd, shell=True)
