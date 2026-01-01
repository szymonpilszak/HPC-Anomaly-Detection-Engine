#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

/**
 * High-performance anomaly detection using Z-Score methodology.
 * Optimized with OpenMP for multi-core parallel processing.
 */
__declspec(dllexport) int detect_anomalies(double* data, int* results, int size, double threshold) {
    if (size <= 0) return -1;

    double sum = 0.0;
    double sq_sum = 0.0;

    // Phase 1: Parallel reduction to calculate mean and variance
    #pragma omp parallel for reduction(+:sum, sq_sum)
    for (int i = 0; i < size; i++) {
        sum += data[i];
        sq_sum += data[i] * data[i];
    }

    double mean = sum / size;
    double variance = (sq_sum / size) - (mean * mean);
    double std_dev = sqrt(variance);

    // Phase 2: Parallel identification of outliers
    #pragma omp parallel for
    for (int i = 0; i < size; i++) {
        double z_score = fabs((data[i] - mean) / std_dev);
        results[i] = (z_score > threshold) ? 1 : 0;
    }

    return 0;
}