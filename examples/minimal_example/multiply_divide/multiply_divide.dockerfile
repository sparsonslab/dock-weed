FROM ubuntu:bionic-20210827

# Install GCC compiler.
RUN apt-get update && apt-get install -y g++-4.8

# Include JSON library.
# https://github.com/nlohmann/json/releases
COPY ./nlohmann/json.hpp ./nlohmann/json.hpp

# For each node:
# ... Copy the source.
COPY multiply.cpp divide.cpp ./

# ... Compile as an app.
RUN g++-4.8 -std=c++11 multiply.cpp -o multiply
RUN g++-4.8 -std=c++11 divide.cpp -o divide

LABEL process.c_multiply="./multiply" process.c_divide="./divide"
