#define BLOCKSIZE 4 * 4
void do_block (double *subC, double *subA, double *subB)
{
    int i, j, k;
    
    for (i = 0; i < BLOCKSIZE; i++)
    for (j = 0; j < BLOCKSIZE; j++)
    for (k = 0; k < BLOCKSIZE; k++)
        subC[i * BLOCKSIZE * 2 + j] += subA[i * BLOCKSIZE * 2 + k] * subB[k * BLOCKSIZE * 2 + j];
}
void dgemm8x8 (double* A, double* B, double* C)
{
    // subA2 = subA + BLOCKSIZE;
    // subB2 = subB +8  * BLOCKSIZE;
    do_block (C, A, B);
    do_block (C, (A) + BLOCKSIZE, (B) + 8 * BLOCKSIZE);

    do_block (C + BLOCKSIZE, A, B + BLOCKSIZE);
    do_block (C + BLOCKSIZE, (A) + BLOCKSIZE, (B + BLOCKSIZE) + 8 * BLOCKSIZE);

    do_block (C + BLOCKSIZE * 8, A + BLOCKSIZE * 8, B);
    do_block (C + BLOCKSIZE * 8, (A + BLOCKSIZE * 8) + BLOCKSIZE, (B) + 8 * BLOCKSIZE);

    do_block (C + BLOCKSIZE * 8 + BLOCKSIZE, A + BLOCKSIZE * 8, B + BLOCKSIZE);
    do_block (C + BLOCKSIZE * 8 + BLOCKSIZE, (A + BLOCKSIZE * 8) + BLOCKSIZE, (B + BLOCKSIZE) + 8 * BLOCKSIZE);

    for ( int sj = 0; sj < 4; sj += 4*4 )
       for ( int si = 0; si < 4; si += 4*4 )
            for ( int sk = 0; sk < 4; sk += 4*4 )
                do_block(si, sj, sk, A, B, C);
}

1 #define BLOCKSIZE 32
2 void do_block (int n, int si, int sj, int sk, double *A, double
3 *B, double *C)
4 {
5  for (int i = si; i < si+BLOCKSIZE; ++i)
6   for (int j = sj; j < sj+BLOCKSIZE; ++j)
7   {
8    double cij = C[i+j*n];/* cij = C[i][j] */
9    for( int k = sk; k < sk+BLOCKSIZE; k++ )
10    cij += A[i+k*n] * B[k+j*n];/* cij+=A[i][k]*B[k][j] */
11   C[i+j*n] = cij;/* C[i][j] = cij */
12  }
13 }
14 void dgemm (int n, double* A, double* B, double* C)
15 {
16  for ( int sj = 0; sj < n; sj += BLOCKSIZE )
17   for ( int si = 0; si < n; si += BLOCKSIZE )
18    for ( int sk = 0; sk < n; sk += BLOCKSIZE )
19     do_block(n, si, sj, sk, A, B, C);
20 }