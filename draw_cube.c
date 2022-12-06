#include <stdio.h>
#include <Windows.h>
#define _USE_MATH_DEFINES // This is required to get M_PI
#include <math.h>


// My terminal width is 160 characters
// and I want 50 characters of height

#define TERMINAL_WIDTH 156
#define TERMINAL_HEIGHT 30

char screen_buffer[TERMINAL_HEIGHT][TERMINAL_WIDTH];
float z_buffer[TERMINAL_HEIGHT][TERMINAL_WIDTH];

int screen_width = TERMINAL_WIDTH;
int screen_height = TERMINAL_HEIGHT;


// ---------------------------------------- Works fine ----------------------------------------
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


// Final zbuffer logic
// // zbuffer is a 2d array of floats
// // it holds the point closest to the camera for each pixel
// // if the point is closer to the camera than the point in the zbuffer
// // then the point is drawn onto the screen_buffer
void final_zbuffer_logic(char c, float z_val, int x, int y) {
    // printf("Should've drawn x: %d, y: %d, z: %f\n", x, y, z_val);

    if (y >= 0 && y < screen_height && x >= 0 && x < screen_width) {
        if (z_val > z_buffer[y][x]) {

            z_buffer[y][x] = z_val;
            screen_buffer[y][x] = c;
        }
    }
}

void clear_zbuffer() {
    memset(z_buffer, 0, screen_width * screen_height * sizeof(float)); // Won't ever draw negative points
}
// ---------------------------------------- Works fine ----------------------------------------


// A point in 3d space, x, y are terminal coordinates, z is depth, positive is toward user
struct POINT3D {
    float x;
    float y;
    float z;
} typedef POINT3D;

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
POINT3D* rotate_point(POINT3D* point, float psi, float theta, float phi) {
    POINT3D* point_rotated = (POINT3D*) malloc(sizeof(POINT3D));
    printf("Rotating point: %f, %f, %f\n", point->x, point->y, point->z);
    point_rotated->x = cos(psi) * cos(theta) * cos(phi) + -sin(psi) * sin(phi) * point->x  +  (cos(psi) * cos(theta) * -sin(phi) + -sin(psi) * cos(phi)) * point->y  +  (cos(psi) * sin(theta)) * point->z;

    point_rotated->y = sin(psi) * cos(theta) * cos(phi) + cos(psi) * sin(phi) * point->x  +  (sin(psi) * cos(theta) * -sin(phi) + cos(psi) * cos(phi)) * point->y  +  (sin(psi) * sin(theta)) * point->z;
    
    point_rotated->z = -sin(theta) * cos(phi) * point->x  +  (-sin(theta) * -sin(phi)) * point->y  +  (cos(theta)) * point->z;

    printf("point_rotated->x: %f, point_rotated->y: %f, point_rotated->z: %f\n", point_rotated->x, point_rotated->y, point_rotated->z);
    return point_rotated;
}


void place_cube_in_z_buffer_rotation(POINT3D center, float width, float psi, float theta, float phi) {
    POINT3D* rot_point_ptr;
    POINT3D point;
    for (float i = -width; i < width; i+=.5) {
        for (float j = -width; j < width; j+=.5) {
            // Only top face
            point = (POINT3D) {i, j, width};
            printf("ij point: %f, %f, %f\n", point.x, point.y, point.z);
            rot_point_ptr = rotate_point(&point, psi, theta, phi);
            printf("rot point: %.2f, %.2f, %.2f, ", rot_point_ptr->x, rot_point_ptr->y, rot_point_ptr->z);

            final_zbuffer_logic('o', rot_point_ptr->z + center.z, rot_point_ptr->x + center.x, rot_point_ptr->y + center.y);
            putchar('\n');
        }
    }
}

int main() {
    float psi = 0, theta = 0, phi = 0;
    float increment = 0;
    POINT3D center = {(float) (screen_width / 2), (float) (screen_height / 2), 100};
    float width = 10;
    clear_zbuffer();
    while (1) {
        // calculate cube
        set_buffer_background('.');
        clear_zbuffer();
        place_cube_in_z_buffer_rotation(center, width, psi, theta, phi);

        // draw cube
        clear_screen();
        set_cursor_top();
        // draw_buffer();

        // sleep
        // psi += increment;
        // theta += increment * 2;
        // phi += increment * 3;
        Sleep(500);

    }
}