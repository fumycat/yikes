#include "utils.h"


int main(int argc, char const* argv[])
{
    /*
        1. int m - A matrix rows & C matrix rows
        2. int n - B matrix columns & C matrix columns
        3. int k - A matrix columns & B matrix rows
        4. float alpha
        5. float beta
        6. const char* - A matrix file
        7. const char* - B matrix file
        8. const char* - C matrix file
        9. const char* - output matrix file
        
        example:
        ./e 3 3 3 1 1 A.txt B.txt C.txt out.txt

        A: m*k
        B: k*n
        C: m*n
    */
    int m = atoi(argv[1]);
    int n = atoi(argv[2]);
    int k = atoi(argv[3]);

    float alpha = atof(argv[4]);
    float beta = atof(argv[5]);

    std::ifstream f0(argv[6]);
    std::ifstream f1(argv[7]);
    std::ifstream f2(argv[8]);
    std::ofstream f3(argv[9]);

    cublasHandle_t handle;

    float* a;
    float* b;
    float* c;

    a = (float*)malloc(m * k * sizeof(float));
    b = (float*)malloc(k * n * sizeof(float));
    c = (float*)malloc(m * n * sizeof(float));

    // read files
    float t;
    int i, j;
    for (i = 0; i < m; i++) {
        for (j = 0; j < k; j++) {
            f0 >> t;
            a[i * k + j] = t;
        }
    }
    for (i = 0; i < k; i++) {
        for (j = 0; j < n; j++) {
            f1 >> t;
            b[i * n + j] = t;
        }
    }
    for (i = 0; i < m; i++) {
        for (j = 0; j < n; j++) {
            f2 >> t;
            c[i * n + j] = t;
        }
    }

    float* d_a;
    float* d_b;
    float* d_c;

    // alocate memory on device
    HANDLE_ERROR(cudaMalloc((void**)&d_a, m * k * sizeof(*a)));
    HANDLE_ERROR(cudaMalloc((void**)&d_b, k * n * sizeof(*b)));
    HANDLE_ERROR(cudaMalloc((void**)&d_c, m * n * sizeof(*c)));

    // create context
    HANDLE_BLERR(cublasCreate(&handle));
    
    // copy host to device
    HANDLE_BLERR(cublasSetMatrix(m, k, sizeof(*a), a, m, d_a, m));
    HANDLE_BLERR(cublasSetMatrix(k, n, sizeof(*b), b, k, d_b, k));
    HANDLE_BLERR(cublasSetMatrix(m, n, sizeof(*c), c, m, d_c, m));

    // matrix multiplication
    HANDLE_BLERR(cublasSgemm(handle, CUBLAS_OP_N, CUBLAS_OP_N, m, n, k, &alpha, d_a, m, d_b, k, &beta, d_c, m));

    // copy device to host
    HANDLE_BLERR(cublasGetMatrix(m, n, sizeof(*c), d_c, m, c, m));

    // write file
    for (i = 0; i < m; i++) {
        for (j = 0; j < n; j++) {
            #ifdef FLOAT_IO_REPR
            f3 << FLOAT_IO_REPR << c[i * n + j] << " ";
            #else
            f3 << c[i * n + j] << " ";
            #endif
        }
        f3 << std::endl;
    }

    cudaFree(d_a);
    cudaFree(d_b);
    cudaFree(d_c);
    cublasDestroy(handle);

    return 0;
}
