

R_y_theta = [
    ["cos(theta)", "0", "sin(theta)"],
    ["0", "1", "0"],
    ["-sin(theta)", "0", "cos(theta)"]
]

R_z_phi = [
    ["cos(phi)", "-sin(phi)", "0"],
    ["sin(phi)", "cos(phi)", "0"],
    ["0", "0", "1"]
]

R_z_psi = [
    ["cos(psi)", "-sin(psi)", "0"],
    ["sin(psi)", "cos(psi)", "0"],
    ["0", "0", "1"]
]

R_x = [
    ["1", "0", "0"],
    ["0", "cos(roll)", "-sin(roll)"],
    ["0", "sin(roll)", "cos(roll)"]
    ]

R_y = [
    ["cos(yaw)", "0", "sin(yaw)"],
    ["0", "1", "0"],
    ["-sin(yaw)", "0", "cos(yaw)"]
]

R_z = [
    ["cos(pitch)", "-sin(pitch)", "0"],
    ["sin(pitch)", "cos(pitch)", "0"],
    ["0", "0", "1"]
]

POINTS = [
    ["x"],
    ["y"],
    ["z"]
]

POINTS_DOT = [
    ["point->x"],
    ["point->y"],
    ["point->z"]
]

def matrix_multiply(A, B, final = False):
    C = [["" for col_size in range(len(B[0]))] for row_size in range(len(A))]
    for row in range(len(A)):
        for col in range(len(B[0])):
            for k in range(len(B)):
                if A[row][k] == "0" or B[k][col] == "0":
                    if k == 0:
                        C[row][col] = "0"
                    continue
                if C[row][col] == "" or C[row][col] == "0":
                    C[row][col] = A[row][k] + " * " + B[k][col]
                else:
                    if final:
                        C[row][col] += "  +  (" + A[row][k] + ") * " + B[k][col]
                    else:
                        C[row][col] += " + " + A[row][k] + " * " + B[k][col]
                

    return C

# in rubato we would need to do Y then Z then Y to get the same result
# for ZYZ rotation

R_all = matrix_multiply(matrix_multiply(R_z_psi, R_y_theta), R_z_phi)
New_points = matrix_multiply(R_all, POINTS_DOT, final = True)

for i in range(len(New_points)):
    New_points[i][0] = New_points[i][0].replace(" 1 *", "")
    New_points[i][0] = New_points[i][0].replace("1 * ", "")
    New_points[i][0] = New_points[i][0].replace(" * 1", "")

print("New_points = for ZYZ rotation")
for row in New_points:
    print(row[0])


# for ZYX rotation
R_all = matrix_multiply(matrix_multiply(R_z, R_y), R_x)
New_points = matrix_multiply(R_all, POINTS, final = True)

for i in range(len(New_points)):
    New_points[i][0] = New_points[i][0].replace(" 1 *", "")
    New_points[i][0] = New_points[i][0].replace("1 * ", "")
    New_points[i][0] = New_points[i][0].replace(" * 1", "")

print("\n\nNew points = for ZYX rotation")
for row in New_points:
    print(row[0])
