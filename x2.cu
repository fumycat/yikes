#include <cuda.h>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

using namespace std;


__global__ void multKernel(float* A, float* B, float* C, int n) {

    int row = blockIdx.y*blockDim.y+threadIdx.y;
    int col = blockIdx.x*blockDim.x+threadIdx.x;

    float tmpSum = 0;

    if (row < n && col < n) {
        for (int i = 0; i < n; i++) {
            tmpSum += A[row * n + i] * B[i * n + col];
        }
    }
    C[row * n + col] = tmpSum;
}


int main(int argc, char const *argv[])
{
    if (argc < 3) {
        cout << "Input file not specified. Please, specify it as a first argument." << endl;
        cout << "example: " << argv[0] << "file0.txt file1.txt" << endl;
        return -1;
    }

    ifstream f0(argv[1]);
    ifstream f1(argv[2]);
    ofstream output("out.txt");
    if (!f0) {
        cout << "f0 err" << endl;
        return -1;
    }
    if (!f1) {
        cout << "f1 err" << endl;
        return -1;
    }

    int n, zn;
    f0 >> n;
    f1 >> zn;
    if (n != zn) {
        cout << "dim error" << endl;
        return -1;
    }

    thrust::host_vector<float> host_a(n * n), host_b(n * n);
    int i = 0;
    float t;
    while (f0 >> t) {
        host_a[i++] = t;
    }
    i = 0;
    while (f1 >> t) {
        host_b[i++] = t;
    }

    thrust::device_vector<float> mat_a(n * n), mat_b(n * n), mat_out(n * n);

    // copy host to device
    mat_a = host_a;
    mat_b = host_b;

    dim3 threadsPerBlock(n, n);
    dim3 blocksPerGrid(1, 1);
    if (n*n > 512){
        threadsPerBlock.x = 512;
        threadsPerBlock.y = 512;
        blocksPerGrid.x = ceil(double(n)/double(threadsPerBlock.x));
        blocksPerGrid.y = ceil(double(n)/double(threadsPerBlock.y));
    }
    multKernel<<<blocksPerGrid,threadsPerBlock>>>(thrust::raw_pointer_cast(&mat_a[0]), thrust::raw_pointer_cast(&mat_b[0]), thrust::raw_pointer_cast(&mat_out[0]), n);


    thrust::host_vector<float> host_out(n * n);
    host_out = mat_out;

    output << n << endl;
    for (int k = 0; k < n; ++k)
    {
        for ( int j = 0; j < n; ++j)
        {
            output << host_out[k * n + j] << " ";
        }
        output << endl;
    }

    // auto delete when function returns
    return 0;
}