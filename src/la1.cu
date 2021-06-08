#include "utils.h"


int main(int argc, char const* argv[])
{
    /*
        1. int m - A matrix rows & y vector len
        2. int n - A matrix columns & x vector len

        3. float alpha
        4. float beta
        5. const char* - A matrix file
        6. const char* - x vector file
        7. const char* - y vector file
        8. const char* - output vector file
        
        example:
        ./e 512 256 A.txt x.txt y.txt out.txt

        A: m*n
        x: n
        y: m
    */
    int m = atoi(argv[1]);
    int n = atoi(argv[2]);

    float alpha = atof(argv[3]);
    float beta = atof(argv[4]);

    std::ifstream f0(argv[5]);
    std::ifstream f1(argv[6]);
    std::ifstream f2(argv[7]);
    std::ofstream f3(argv[8]);

    cublasHandle_t handle;

    float* a;
    float* x;
    float* y;

    a = (float*)malloc(m * n * sizeof(float));
    x = (float*)malloc(n * sizeof(float));
    y = (float*)malloc(m * sizeof(float));

    // read files
    float t;
    int i, j;
    for (i = 0; i < m; i++) {
        for (j = 0; j < n; j++) {
            f0 >> t;
            a[i * n + j] = t;
        }
    }
    for (i = 0; i < n; i++) {
        f1 >> t;
        x[i] = t;
    }
    for (i = 0; i < m; i++) {
        f2 >> t;
        y[i] = t;
    }

    float* d_a;
    float* d_x;
    float* d_y;

    // alocate memory on device
    HANDLE_ERROR(cudaMalloc((void**)&d_a, m * n * sizeof(*a)));
    HANDLE_ERROR(cudaMalloc((void**)&d_x, n * sizeof(*x)));
    HANDLE_ERROR(cudaMalloc((void**)&d_y, m * sizeof(*y)));

    // create context
    HANDLE_BLERR(cublasCreate(&handle));
    
    // copy host to device
    HANDLE_BLERR(cublasSetMatrix(m, n, sizeof(*a), a, m, d_a, m));
    HANDLE_BLERR(cublasSetVector(n, sizeof(*x), x, 1, d_x, 1));
    HANDLE_BLERR(cublasSetVector(m, sizeof(*y), y, 1, d_y, 1));

    // gemv
    HANDLE_BLERR(cublasSgemv(handle, CUBLAS_OP_N, m, n, &alpha, d_a, m, d_x, 1, &beta, d_y, 1));

    // copy device to host
    HANDLE_BLERR(cublasGetVector(m, sizeof(*y), d_y, 1, y, 1));

    // write file
    for (i = 0; i < m; i++) {
        #ifdef FLOAT_IO_REPR
        f3 << FLOAT_IO_REPR << y[i];
        #else
        f3 << y[i];
        #endif
        if (i == m - 1) 
            f3 << std::endl;
        else
            f3 << " ";
    }

    cudaFree(d_a);
    cudaFree(d_x);
    cudaFree(d_y);
    cublasDestroy(handle);

    return 0;
}
