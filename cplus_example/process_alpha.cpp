#include <iostream>
#define JSON_SKIP_UNSUPPORTED_COMPILER_CHECK 1
#include "nlohmann/json.hpp"
using namespace nlohmann;

int main() {

    try {
        // Parse std::in to JSON
        json inputData;
        std::cin >> inputData;

        // Get parameters from JSON.
        float a;
        float b;
        inputData.at("a").get_to(a);
        inputData.at("b").get_to(b);

        // Output.
        json outputData;
        outputData["z"] = a + b;
        std::cout << outputData << std::endl;
        return 0;
    }
    catch (json::parse_error& ex) {}   // If std::cin cannot be parsed as JSON.
    catch (json::out_of_range& ex) {}  // If parameter keys do not exist.

    json defaultArgs;
    defaultArgs = json::parse(R"({"input": {"a": 1.0, "b": 1.0}, "output": {"z": 1.0}})");
    std::cout << defaultArgs << std::endl;
    return 0;
}
