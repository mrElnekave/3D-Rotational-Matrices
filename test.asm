.data 


# matrix stored in memory
.align 2
matrixZ: .word 
1, 2, 3, 4, 5, 6, 7, 8,
1, 2, 3, 4, 5, 6, 7, 8,
8, 7, 6, 5, 4, 3, 2, 1,
8, 7, 6, 5, 4, 3, 2, 1,
1, 0, 0, 0, 0, 0, 0, 0,
0, 2, 3, 0, 0, 0, 1, 0,
0, 0, 0, 0, 0, 2, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0

matrixY: .word
1, 0, 0, 0, 0, 0, 0, 0,
0, 1, 0, 0, 0, 0, 0, 0,
0, 0, 1, 0, 0, 0, 0, 0,
1, 0, 0, 1, 0, 0, 0, 0,
0, 0, 0, 0, 1, 0, 0, 0,
0, 0, 0, 0, 0, 1, 0, 0,
0, 0, 0, 0, 0, 0, 1, 0,
0, 0, 0, 0, 0, 1, 1, 0


matrixX: .space 256  # 64 * 4
matrix_row_length: .word 32

.align 2
new_line: .asciiz "\n"
.align 2
SPACE: .asciiz " "

.text

j main
# --------------------------------------------------------------start matrix multiplication

mm_4x4:
# $a0 = x_adress, $a1 = y_adress, $a2 = z_adress

# key
# $t0, used for calculating position of value in matrix
# $t1, used for size of row
# $t2, saved for x[i][j] address
# $t9, sotres x[i][j]
# $t8, stores z[i][k]
# $t7, stores y[i][k]
    # save $ra
    addi $sp, $sp, -4  # not actually needed but I might call a procedure later on.
    sw $ra, 0($sp)

    li   $t1, 4            # $t1 = 4 (row size/loop end)
    li   $s0, 0            # i = 0; initialize 1st for loop
    L1: li   $s1, 0        # j = 0; restart 2nd for loop
        L2: li   $s2, 0        # k = 0; restart 3rd for loop

            # find x[i][j] address and load it into $t9
            sll $t2, $s0, 2    # $t2 = i * 4 (size of row of x)
            addu $t2, $t2, $s1 # $t2 = i * size(row) + j
            sll  $t2, $t2, 2   # $t2 = byte offset of [i][j], how muny bytes to store a number. 4 bytes to a 32 word.
            addu $t2, $a0, $t2 # $t2 = byte address of x[i][j], add adress of matrix 1
            lw  $t9, 0($t2)    # $t9 = 4 bytes of x[i][j]
        
            L3: # find y[j][k] address and load it into $t7, find z[i][k] address and load it into $t8, multiply and add to t9 and store it back into t9
                sll  $t0, $s2, 2   # $t0 = k * 4 (size of row of z)
                addu $t0, $t0, $s1 # $t0 = k * size(row) + j
                sll  $t0, $t0, 2   # $t0 = byte offset of [k][j]
                addu $t0, $a2, $t0 # $t0 = byte address of z[k][j]
                lw  $t8, 0($t0)    # $t8 = 4 bytes of z[k][j]


                sll   $t0, $s0, 2      # $t0 = i*4 (size of row of y)
                addu  $t0, $t0, $s2    # $t0 = i*size(row) + k
                sll   $t0, $t0, 2      # $t0 = byte offset of [i][k]
                addu  $t0, $a1, $t0    # $t0 = byte address of y[i][k]
                lw   $t7, 0($t0)       # $t7 = 4 bytes of y[i][k]
                
                
                mul $t8, $t7, $t8      # $t8 = y[i][k] * z[k][j]
                add $t9, $t9, $t8      # t9=x[i][j] + y[i][k]*z[k][j]

                addiu $s2, $s2, 1      # $k k + 1
                bne   $s2, $t1, L3     # if (k != 4) go to L3
            
            sw   $t9, 0($t2)       # x[i][j] = $t9

            addiu $s1, $s1, 1      # $j = j + 1
            bne   $s1, $t1, L2     # if (j != 4) go to L2
        
        
        addiu $s0, $s0, 1      # $i = i + 1
        bne   $s0, $t1, L1     # if (i != 4) go to L1
    
    # restore $ra
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra

# pseudo code
# void mm (double x[][],
#         double y[][], double z[][]) {
#  int i, j, k;
#  for (i = 0; i! = 32; i = i + 1)
#    for (j = 0; j! = 32; j = j + 1)
#      for (k = 0; k! = 32; k = k + 1)
#        x[i][j] = x[i][j]
#                  + y[i][k] * z[k][j];
#}


# --------------------------------------------------------------end matrix multiplication

# --------------------------------------------------------------start matrix multiplication 8x8

mm_8x8:
# $a0 = x_adress, $a1 = y_adress, $a2 = z_adress

# key
# $t0, used for calculating position of value in matrix
# $t1, used for size of row
# $t2, saved for x[i][j] address
# $t9, sotres x[i][j]
# $t8, stores z[i][k]
# $t7, stores y[i][k]
    # save $ra
    addi $sp, $sp, -4  # not actually needed but I might call a procedure later on.
    sw $ra, 0($sp)

    li   $t1, 8            # $t1 = 8 (row size/loop end)
    li   $s0, 0            # i = 0; initialize 1st for loop
    L1_8: li   $s1, 0        # j = 0; restart 2nd for loop
        L2_8: li   $s2, 0        # k = 0; restart 3rd for loop

            # find x[i][j] address and load it into $t9
            sll $t2, $s0, 3    # $t2 = i * 8 (size of row of x)
            addu $t2, $t2, $s1 # $t2 = i * size(row) + j
            sll  $t2, $t2, 2   # $t2 = byte offset of [i][j], how muny bytes to store a number. 4 bytes to a 32 word.
            addu $t2, $a0, $t2 # $t2 = byte address of x[i][j], add adress of matrix 1
            lw  $t9, 0($t2)    # $t9 = 4 bytes of x[i][j]
        
            L3_8: # find y[j][k] address and load it into $t7, find z[i][k] address and load it into $t8, multiply and add to t9 and store it back into t9
                sll  $t0, $s2, 3   # $t0 = k * 8 (size of row of z)
                addu $t0, $t0, $s1 # $t0 = k * size(row) + j
                sll  $t0, $t0, 2   # $t0 = byte offset of [k][j]
                addu $t0, $a2, $t0 # $t0 = byte address of z[k][j]
                lw  $t8, 0($t0)    # $t8 = 4 bytes of z[k][j]


                sll   $t0, $s0, 3      # $t0 = i*8 (size of row of y)
                addu  $t0, $t0, $s2    # $t0 = i*size(row) + k
                sll   $t0, $t0, 2      # $t0 = byte offset of [i][k]
                addu  $t0, $a1, $t0    # $t0 = byte address of y[i][k]
                lw   $t7, 0($t0)       # $t7 = 4 bytes of y[i][k]
                
                
                mul $t8, $t7, $t8      # $t8 = y[i][k] * z[k][j]
                add $t9, $t9, $t8      # t9=x[i][j] + y[i][k]*z[k][j]

                addiu $s2, $s2, 1      # $k k + 1
                bne   $s2, $t1, L3_8     # if (k != 4) go to L3
            
            sw   $t9, 0($t2)       # x[i][j] = $t9

            addiu $s1, $s1, 1      # $j = j + 1
            bne   $s1, $t1, L2_8     # if (j != 4) go to L2
        
        
        addiu $s0, $s0, 1      # $i = i + 1
        bne   $s0, $t1, L1_8     # if (i != 4) go to L1
    
    # restore $ra
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra

# pseudo code
# void mm (double x[][],
#         double y[][], double z[][]) {
#  int i, j, k;
#  for (i = 0; i! = 32; i = i + 1)
#    for (j = 0; j! = 32; j = j + 1)
#      for (k = 0; k! = 32; k = k + 1)
#        x[i][j] = x[i][j]
#                  + y[i][k] * z[k][j];
#}


# --------------------------------------------------------------end matrix multiplication 8x8 


# --------------------------------------------------------------start matrix multiplication 8x8 blocked

mm_4x4B:
# $a0 = x_adress, $a1 = y_adress1, $a2 = z_adress

# key
# $s0 = i, $s1 = j, $s2 = k
# $s3 = x_adress, $s4 = y_adress2, $s5 = z_adress

# $t0, used for calculating position of value in matrix
# $t1, used for size of row
# $t2, saved for x[i][j] address
# $t9, stores x[i][j]
# $t8, stores z[i][k]
# $t7, stores y[i][k]
    # save $ra
    addi $sp, $sp, -4  # not actually needed but I might call a procedure later on.
    sw $ra, 0($sp)
    # save s0, s1, s2
    addi $sp, $sp, -12
    sw $s0, 0($sp)
    sw $s1, 4($sp)
    sw $s2, 8($sp)


    li   $t1, 4            # $t1 = 4 (row size/loop end)
    li   $s0, 0            # i = 0; initialize 1st for loop
    L1B: li   $s1, 0        # j = 0; restart 2nd for loop
        L2B: li   $s2, 0        # k = 0; restart 3rd for loop

            # find x[i][j] address and load it into $t9
            # i * BLOCKSIZE * 2 + j
            sll $t2, $s0, 3    # $t2 = i * 4 (size of row of x) * 2 (2 blocks per row)
            addu $t2, $t2, $s1 # $t2 = i * size(row) + j
            sll  $t2, $t2, 2   # $t2 = byte offset of [i][j], how muny bytes to store a number. 4 bytes to a 32 word.
            addu $t2, $a0, $t2 # $t2 = byte address of x[i][j], add adress of matrix 1
            lw  $t9, 0($t2)    # $t9 = 4 bytes of x[i][j]
        
            L3B: # find y[i][k] address and load it into $t7, find z[k][j] address and load it into $t8, multiply and add to t9 and store it back into t9
                sll  $t0, $s2, 3   # $t0 = k * 4 (size of row of z) * 2 (2 blocks per row)
                addu $t0, $t0, $s1 # $t0 = k * size(row) + j
                sll  $t0, $t0, 2   # $t0 = byte offset of [k][j]
                addu $t0, $a2, $t0 # $t0 = byte address of z[k][j]
                lw  $t8, 0($t0)    # $t8 = 4 bytes of z[k][j]


                sll   $t0, $s0, 3      # $t0 = i * 4 (size of row of y) * 2 (2 blocks per row)
                addu  $t0, $t0, $s2    # $t0 = i * size(row) + k
                sll   $t0, $t0, 2      # $t0 = byte offset of [i][k]
                addu  $t0, $a1, $t0    # $t0 = byte address of y[i][k]
                lw   $t7, 0($t0)       # $t7 = 4 bytes of y[i][k]
                
                
                mul $t8, $t7, $t8      # $t8 = y[i][k] * z[k][j]
                add $t9, $t9, $t8      # t9=x[i][j] + y[i][k]*z[k][j]

                addiu $s2, $s2, 1      # $k k + 1
                bne   $s2, $t1, L3B     # if (k != 4) go to L3
            
            sw   $t9, 0($t2)       # x[i][j] = $t9

            addiu $s1, $s1, 1      # $j = j + 1
            bne   $s1, $t1, L2B     # if (j != 4) go to L2
        
        
        addiu $s0, $s0, 1      # $i = i + 1
        bne   $s0, $t1, L1B     # if (i != 4) go to L1
    
    # restore s0, s1, s2
    lw $s0, 0($sp)
    lw $s1, 4($sp)
    lw $s2, 8($sp)
    addi $sp, $sp, 12
    # restore $ra
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra


mm_8x8B:
# $a0 = x_adress, $a1 = y_adress, $a2 = z_adress   
# $s0 = x_adress, $s1 = y_adress, $s2 = z_adress

    addi $sp, $sp, -4  
    sw $ra, 0($sp)

    # calculate all positions
    move $s0, $a0 # $s0 = X1
    move $s1, $a1 # $s1 = Y1
    move $s2, $a2 # $s2 = Z1
    
    # base + 4*4 = base + 16 = M2
    # base + 4*4*2*4 = base + 128 = M3
    # base + 4*4*2*4 + 4*4 = base + 144 = M4


#     do_block (C, A, B); C1
# C1 += A1 * B1
    jal mm_4x4B
 
#     do_block (C + BLOCKSIZE, A, B + BLOCKSIZE); C2 
# C2 += A1 * B2
    add $a0, $s0, 16  # 4 * 4 C2
    move $a1, $s1  # A1
    add $a2, $s2, 16  # 4 * 4 B2
    jal mm_4x4B   



#     do_block (C, A1, (B) + 8 * BLOCKSIZE); C1
# C1 += A2 * B3 
    move $a0, $s0  # C1
    add $a1, $s1, 16  # 4 * 4 A2
    add $a2, $s2, 128  # 8 * 4 * 4 B3

    jal mm_4x4B

#     do_block (C + BLOCKSIZE, (A) + BLOCKSIZE, (B + BLOCKSIZE) + 8 * BLOCKSIZE); C2
# C2 += A2 * B4
    add $a0, $s0, 16  # 4 * 4 C2
    add $a1, $s1, 16  # 4 * 4 A2
    add $a2, $s2, 144  # 8 * 4 * 4 + 4 * 4 B4
    jal mm_4x4B



#     do_block (C + BLOCKSIZE * 8, A + BLOCKSIZE * 8, B);
# C3 += A3 * B1
    add $a0, $s0, 128  # 8 * 4 * 4 C3
    add $a1, $s1, 128  # 8 * 4 * 4 A3
    move $a2, $s2  # B1
    jal mm_4x4B

#     do_block (C + BLOCKSIZE * 8 + BLOCKSIZE, A + BLOCKSIZE * 8, B + BLOCKSIZE);
# C4 += A3 * B2
    add $a0, $s0, 144  # 8 * 4 * 4 + 4 * 4 C4
    add $a1, $s1, 128  # 8 * 4 * 4 A3
    add $a2, $s2, 16  # 4 * 4 B2
    jal mm_4x4B



#     do_block (C + BLOCKSIZE * 8, (A + BLOCKSIZE * 8) + BLOCKSIZE, (B) + 8 * BLOCKSIZE);
# C3 += A4 * B3
    add $a0, $s0, 128  # 8 * 4 * 4 C3
    add $a1, $s1, 144  # 8 * 4 * 4 + 4 * 4 A4
    add $a2, $s2, 128  # 8 * 4 * 4 B3
    jal mm_4x4B

#     do_block (C + BLOCKSIZE * 8 + BLOCKSIZE, (A + BLOCKSIZE * 8) + BLOCKSIZE, (B + BLOCKSIZE) + 8 * BLOCKSIZE);
# C4 += A4 * B4
    add $a0, $s0, 144  # 8 * 4 * 4 + 4 * 4 C4
    add $a1, $s1, 144  # 8 * 4 * 4 + 4 * 4 A4
    add $a2, $s2, 144  # 8 * 4 * 4 + 4 * 4 B4
    jal mm_4x4B

    # restore $ra
    lw $ra, 0($sp)
    addi $sp, $sp, 4
    jr $ra





# void do_block (double *subC, double *subA, double *subB)
# {
#     int i, j, k;
    
#     for (i = 0; i < BLOCKSIZE; i++)
#     for (j = 0; j < BLOCKSIZE; j++)
#     for (k = 0; k < BLOCKSIZE; k++)
#         subC[i * BLOCKSIZE * 2 + j] += subA[i * BLOCKSIZE * 2 + k] * subB[k * BLOCKSIZE * 2 + j];
# }
# void dgemm8x8 (double* A, double* B, double* C)
# {
#     // subA2 = subA + BLOCKSIZE;
#     // subB2 = subB +8  * BLOCKSIZE;
#     do_block (C, A, B);
#     do_block (C, (A) + BLOCKSIZE, (B) + 8 * BLOCKSIZE);

#     do_block (C + BLOCKSIZE, A, B + BLOCKSIZE);
#     do_block (C + BLOCKSIZE, (A) + BLOCKSIZE, (B + BLOCKSIZE) + 8 * BLOCKSIZE);

#     do_block (C + BLOCKSIZE * 8, A + BLOCKSIZE * 8, B);
#     do_block (C + BLOCKSIZE * 8, (A + BLOCKSIZE * 8) + BLOCKSIZE, (B) + 8 * BLOCKSIZE);

#     do_block (C + BLOCKSIZE * 8 + BLOCKSIZE, A + BLOCKSIZE * 8, B + BLOCKSIZE);
#     do_block (C + BLOCKSIZE * 8 + BLOCKSIZE, (A + BLOCKSIZE * 8) + BLOCKSIZE, (B + BLOCKSIZE) + 8 * BLOCKSIZE);
# }

# --------------------------------------------------------------end matrix multiplication 8x8 blocked

# --------------------------------------------------------------start matrix print
matrix_print:
# $a0 = matrix adress, $a1 row size
# $t0, used for calculating position of value in matrix
# $t1, used for size of row
    move $t1, $a1            # $t1 = (row size/loop end)
    li   $s0, 0            # i = 0; initialize 1st for loop
    move $s7, $a0	    # store matrix base address.
    
    li $v0, 4  # printing new line
    la $a0, new_line
    syscall
    
    L1P: li   $s1, 0       # j = 0; restart 2nd for loop
        L2P: sll  $t0, $s0, 3  # $t0 = i * 4 (size of row of x)
            addu $t0, $t0, $s1 # $t0 = i * size(row) + j
            sll  $t0, $t0, 2   # $t0 = byte offset of [i][j], how muny bytes to store a number. 4 bytes to a 32 word.
            addu $t0, $s7, $t0 # $t0 = byte address of x[i][j], add adress of matrix 1
            lw   $t9, 0($t0)   # $t9 = 4 bytes of x[i][j]
        
            li $v0, 1  # printing integer
            move $a0, $t9
            syscall
            
            li $v0, 4  # printing space
            la $a0, SPACE
            syscall
            
            addiu $s1, $s1, 1      # $j = j + 1
            bne   $s1, $t1, L2P    # if (j != 4) go to L2
        
        li $v0, 4  # printing new line
        la $a0, new_line
        syscall
        
        addiu $s0, $s0, 1      # $i = i + 1
        bne   $s0, $t1, L1P    # if (i != 4) go to L1
    
    jr $ra

# --------------------------------------------------------------end matrix print

# --------------------------------------------------------------start main
main:

    # call matrix multiplication
    la $a0, matrixX
    la $a1, matrixY
    la $a2, matrixZ
    jal mm_8x8

    # print matrix x
    la $a0, matrixX
    li $a1, 8
    jal matrix_print
    
    la $a0, matrixY
    li $a1, 8
    jal matrix_print
    

# --------------------------------------------------------------end main



# COMMENTARY:
# We can see that using the unroll we use 4 times the number of registers
# and we have 4 times the number of instructions. 
# But we can do these calculations in parrallel if we have multiple CPUs.
# The conceptual complexity is still O(n^3) but the actual complexity is
# O(n^2) because we can do 4 calculations at the same time.
# I think that hypothetically we can unroll again and go to O(1) time but with need for huge parallelization. And many many cores.


# On regular 8x8 matrix mult I had a 50% hit rate.
# 2 way associativity yields a 55% hit rate. So does a 4 way.
# An 8 way associative cach yields 58% hit rate.
# it took 1574 accesses


# Cache size
# block size 
# associativity
# get a hit rate of 95% by playing around with these variables
