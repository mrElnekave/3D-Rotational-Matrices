#include <stdio.h>
#include <Windows.h>
#define _USE_MATH_DEFINES // This is required to get M_PI
#include <math.h>

#define TERMINAL_WIDTH 159
#define TERMINAL_HEIGHT 30

char screen_buffer[TERMINAL_HEIGHT][TERMINAL_WIDTH];
float z_buffer[TERMINAL_HEIGHT][TERMINAL_WIDTH];

int screen_width = TERMINAL_WIDTH;
int screen_height = TERMINAL_HEIGHT;

// Make a 3d rotational cube
struct POINT3D {
    int x;
    int y;
    int z;
};

void clear_screen() {
    printf("\x1b[2J"); // found this clears screen for most op systems

    // for other op systems looks at this
    //https://stackoverflow.com/questions/3646240/how-to-clear-the-screen-with-x1b2j
    // find a way to download and link packages c.

}
void set_cursor_top() {
    printf("\x1b[H");
}
void set_buffer_background(char background) {
    memset(screen_buffer, background, screen_width * screen_height);
}
void draw_buffer() {
    for (int i = 0; i < screen_height; i++) {
        screen_buffer[i][screen_width - 1] = '|';
        for (int j = 0; j < screen_width; j++) {
            putchar(screen_buffer[i][j]);
        }
        putchar('\n');
    }
}



// // Rotation with Euler matrices happens in three steps. Z rotation (twist) (psi), then Y rotation (lean) (theta), then Z rotation (swing) (phi).
// /**
//  * @brief will rotate the cube with a 3d rotational matrix
//  * 
//  * @param point The point to rotate
//  * @param psi The angle to rotate around the z axis (twist)
//  * @param theta The angle to rotate around the y axis (lean)
//  * @param phi The angle to rotate around the z axis (swing)
//  * @return struct POINT3D The rotated point
//  */
// struct POINT3D rotate_point(struct POINT3D point, float psi, float theta, float phi) {
//     struct POINT3D point_rotated;
//     point_rotated.x = cos(theta) * point.x + sin(theta) * sin(psi) * point.y + sin(theta) * cos(psi) * point.z;
//     point_rotated.y = sin(theta) * sin(phi) * point.x + (cos(psi) * cos(phi) - cos(theta) * sin(psi) * sin(phi)) * point.y + (-cos(phi)*sin(psi) - cos(theta)*cos(psi)*cos(phi)) * point.z;
//     point_rotated.z = -sin(theta) * cos(phi) * point.x + (cos(psi) * sin(phi) + cos(theta) * cos(phi) * sin(psi)) * point.y + (-sin(psi) * sin(phi) + cos(theta) * cos(psi) * cos(phi)) * point.z;
    
//     return point_rotated;
// }

// Rotation with Euler matrices happens in three steps. Z rotation (twist) (psi), then Y rotation (lean) (theta), then Z rotation (swing) (phi).
/**
 * @brief will rotate the cube with a 3d rotational matrix
 * 
 * @param point The point to rotate
 * @param psi The angle to rotate around the z axis (twist)
 * @param theta The angle to rotate around the y axis (lean)
 * @param phi The angle to rotate around the z axis (swing)
 * @return struct POINT3D The rotated point
 */
struct POINT3D rotate_point(struct POINT3D point, float psi, float theta, float phi) {
    struct POINT3D point_rotated;
    point_rotated.x = cos(theta) * point.x + 
    sin(theta) * sin(psi) * point.y + 
    sin(theta) * cos(psi) * point.z;

    point_rotated.y = sin(theta) * sin(phi) * point.x + 
    (cos(psi) * cos(phi) - cos(theta) * sin(psi) * sin(phi)) * point.y + 
    (-cos(phi)*sin(psi) - cos(theta)*cos(psi)*sin(phi)) * point.z;

    point_rotated.z = -sin(theta) * cos(phi) * point.x + 
    (cos(psi) * sin(phi) + cos(theta) * cos(phi) * sin(psi)) * point.y + 
    (-sin(psi) * sin(phi) + cos(theta) * cos(psi) * cos(phi)) * point.z;
    
    return point_rotated;
}

int main() {
    float psi = 0, theta = 0, phi = 0;
    float increment = M_PI / 32 ;
    struct POINT3D center = {20, 0, 0};
    struct POINT3D testPoints[4] = {{0, 10, 0}, {-1, 10, 0}, {1, 10, 0}, {1, 9, 0}};
    // clear_zbuffer();

    // rotate psi, then theta, then phi
    while (1) {
        // calculate cube
        set_buffer_background('.');

        // draw points to screen
        for (int i = 0; i < 4; i++) {
            struct POINT3D point = rotate_point(testPoints[i], psi, theta, phi);
            point.x += center.x;
            screen_buffer[point.y][point.x] = 'X';
        }

        screen_buffer[center.y][center.x] = 'O';

        // place_cube_in_z_buffer_rotation(center, 10, psi, theta, phi);

        // draw cube
        clear_screen();
        set_cursor_top();
        draw_buffer();

        // sleep
        psi += increment;
        // theta += increment * 2;
        // phi += increment * 3;
        Sleep(200);

    }
}