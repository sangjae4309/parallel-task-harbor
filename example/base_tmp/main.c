#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char* argv[]) {

    const int size = atoi(argv[1]);
    int first[size][size], second[size][size], multiply[size][size];

    //printf("Populating the first and second matrix...\n");
    for(int x=0; x<size; x++)
    {
        for(int y=0; y<size; y++)
        {
            first[x][y] = x + y;
            second[x][y] = (4 * x) + (7 * y);
        }
    }

    //printf("Multiplying the matrixes...\n");
    clock_t nclk_s = clock();
    for(int c=0; c<size; c++)
    {
        for(int d=0; d<size; d++)
        {
            int sum = 0;
            for(int k=0; k<size; k++)
            {
                sum += first[c][k] * second[k][d];
            }
           multiply[c][d] = sum;
        }
    }
    clock_t nclk_e = clock();

    //printf("Calculating the sum of all elements in the matrix...\n");
    long int sum = 0;
    for(int x=0; x<size; x++)
        for(int y=0; y<size; y++)
            sum += multiply[x][y];

    printf("matrix_mul: size=%d time=%ldclk, the sum is %ld\n", 
            size, nclk_e-nclk_s, sum);
}
