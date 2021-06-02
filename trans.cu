#include <thrust/device_vector.h>
#include <thrust/host_vector.h>
#include <thrust/execution_policy.h>
#include <thrust/transform.h>
#include <thrust/sequence.h>
#include <thrust/copy.h>
#include <thrust/fill.h>
#include <thrust/replace.h>
#include <thrust/functional.h>
#include <iostream>
#include <fstream>

// #include "functor.h"

int main(int argc, char const *argv[])
{
    std::ofstream fs("values.txt");

    thrust::device_vector<float> X(1000000);
    thrust::device_vector<float> Y(1000000);

    thrust::sequence(X.begin(), X.end());
    thrust::fill(Y.begin(), Y.end(), 1.5);

    // thrust::sequence(Y.begin(), Y.end());

    // thrust::transform(X.begin(), X.end(), Y.begin(), thrust::negate<int>());
    // float A = 1.0;

    thrust::transform(X.begin(), X.end(), Y.begin(), Y.begin(), thrust::multiplies<float>());

    thrust::copy(Y.begin(), Y.end(), std::ostream_iterator<float>(fs, " "));

}
