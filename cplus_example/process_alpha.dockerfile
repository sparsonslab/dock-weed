FROM ubuntu:bionic-20210827

# Install GCC compiler.
RUN apt-get update && apt-get install -y g++-4.8

# Include JSON library.
# https://github.com/nlohmann/json/releases
COPY json.hpp ./nlohmann/json.hpp

# For each node:
# ... Copy the source.
COPY process_alpha.cpp .
# ... Compile as an app.
RUN g++-4.8 -std=c++11 process_alpha.cpp -o process_alpha
# ... Label to be recognised as node.
LABEL node.process_alpha="./process_alpha"
