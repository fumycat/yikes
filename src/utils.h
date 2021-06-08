#ifndef __UTILS_H__
#define __UTILS_H__
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include "cublas_v2.h"

// #define FLOAT_IO_REPR std::fixed

static void HandleError( cudaError_t err,
                         const char *file,
                         int line ) {
    if (err != cudaSuccess) {
        printf( "%s in %s at line %d\n", cudaGetErrorString( err ),
                file, line );
        exit( EXIT_FAILURE );
    }
}

#define HANDLE_ERROR( err ) (HandleError( err, __FILE__, __LINE__ ))

static void HandleCublasError( cublasStatus_t err,
                               const char *file,
                               int line ) {
    if (err != CUBLAS_STATUS_SUCCESS) {
        printf( "Cublas error in %s at line %d\n", file, line );
        exit( EXIT_FAILURE );
    }
}

#define HANDLE_BLERR( err ) (HandleCublasError( err, __FILE__, __LINE__ ))

#endif
