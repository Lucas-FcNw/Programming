
#include <algorithm>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<double> values;
    double value;

    std::cout << "Enter numeric values (Ctrl+D to finish):\n";

    while (std::cin >> value) {
        values.push_back(value);
    }

    if (values.empty()) {
        std::cerr << "Error: no values provided.\n";
        return 1;
    }

    const double total =
        std::accumulate(values.begin(), values.end(), 0.0);

    const auto [minimum, maximum] =
        std::minmax_element(values.begin(), values.end());

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Count: " << values.size() << '\n';
    std::cout << "Mean: " << total / values.size() << '\n';
    std::cout << "Minimum: " << *minimum << '\n';
    std::cout << "Maximum: " << *maximum << '\n';

    return 0;
}
