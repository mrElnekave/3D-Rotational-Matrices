

# R_z = [
#     ["1", "0", "0"],
#     ["0", "cos(psi)", "-sin(psi)"],
#     ["0", "sin(psi)", "cos(psi)"]
#     ]

# R_y = [
#     ["cos(theta)", "0", "sin(theta)"],
#     ["0", "1", "0"],
#     ["-sin(theta)", "0", "cos(theta)"]
# ]

# R_x = [
#     ["cos(phi)", "-sin(phi)", "0"],
#     ["sin(phi)", "cos(phi)", "0"],
#     ["0", "0", "1"]
# ]

R_z = [
    ["1", "0", "0"],
    ["0", "cos(roll)", "-sin(roll)"],
    ["0", "sin(roll)", "cos(roll)"]
    ]

R_y = [
    ["cos(yaw)", "0", "sin(yaw)"],
    ["0", "1", "0"],
    ["-sin(yaw)", "0", "cos(yaw)"]
]

R_x = [
    ["cos(pitch)", "-sin(pitch)", "0"],
    ["sin(pitch)", "cos(pitch)", "0"],
    ["0", "0", "1"]
]

POINTS = [
    ["x"],
    ["y"],
    ["z"]
]

def matrix_multiply(A, B, final = False):
    C = [["" for col_size in range(len(B[0]))] for row_size in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                if A[i][k] == "0" or B[k][j] == "0":
                    if k == 0:
                        C[i][j] = "0"
                    continue
                if C[i][j] == "" or C[i][j] == "0":
                    C[i][j] = A[i][k] + " * " + B[k][j]
                else:
                    if final:
                        C[i][j] += "  +  (" + A[i][k] + ") * " + B[k][j]
                    else:
                        C[i][j] += " + " + A[i][k] + " * " + B[k][j]
                

    return C

# in rubato we would need to do Y then Z then Y to get the same result
R_all = matrix_multiply(matrix_multiply(R_x, R_y), R_z)
New_points = matrix_multiply(R_all, POINTS, final = True)

for i in range(len(New_points)):
    New_points[i][0] = New_points[i][0].replace(" 1 *", "")
    New_points[i][0] = New_points[i][0].replace("1 * ", "")
    New_points[i][0] = New_points[i][0].replace(" * 1", "")

for row in New_points:
    print(row[0])

# for row in R_all:
#     print(row)