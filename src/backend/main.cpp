#include <cmath>
#include <iostream>
#include <limits>
#include "body.h"
#include "vector.h"

int main()
{
    SSTP::Body body {SSTP::Vector{{2, 1}}, 2, 0.7};

    constexpr int N = 1000;
    for (int i = 0; i < N; i++) {
        body.set_angle(2 * i * M_PI / N);
        std::cout << body.position() << std::endl;
    }
}