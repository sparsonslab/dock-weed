# Minimal example

A simple example of four nodes for the basic mathematical operators - add, subtract,
multiply, divide. The first two come from a Python image and the last two from a C++ image.


### Build the images.
```
docker build -t add_subtract -f add_subtract/add_subtract.dockerfile ./add_subtract

docker build -t multiple_divide -f multiply_divide/multiply_divide.dockerfile ./multiply_divide
```



### References

Docker command line reference.<br>
https://docs.docker.com/reference/cli/docker/

Docker file reference.<br>
https://docs.docker.com/reference/dockerfile

Niels Lohmann's JSON library for C++.<br>
https://github.com/nlohmann/json


