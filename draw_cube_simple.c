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



// Rotation with Euler matrices happens in three steps. Z rotation (twist) (psi), then Y rotation (lean) (theta), then Z rotation (swing) (phi).

float rotate_x(float x, float y, float z, float psi, float theta, float phi) {
    return cos(theta) * x + sin(theta) * sin(psi) * y + sin(theta) * cos(psi) * z;
}

float rotate_y(float x, float y, float z, float psi, float theta, float phi) {
    return sin(theta) * sin(phi) * x + (cos(psi) * cos(phi) - cos(theta) * sin(psi) * sin(phi)) * y + (cos(psi) * sin(phi) + cos(theta) * cos(phi) * sin(psi)) * z;
}

float rotate_z(float x, float y, float z, float psi, float theta, float phi) {
    return -sin(theta) * cos(phi) * x + (cos(psi) * sin(phi) + cos(theta) * cos(phi) * sin(psi)) * y + (-sin(psi) * sin(phi) + cos(theta) * cos(psi) * cos(phi)) * z;
}

void place_cube_in_z_buffer_rotation(float center_x, float center_y, float center_z, float width, float psi, float theta, float phi) {
    float x, y, z;
    for (float i = -width; i < width; i+=.5) {
        for (float j = -width; j < width; j+=.5) {
            // Only top face
            x = rotate_x(i, j, width, psi, theta, phi);
            y = rotate_y(i, j, width, psi, theta, phi);
            z = rotate_z(i, j, width, psi, theta, phi);
            final_zbuffer_logic('o', z + center_z, center_x + x, center_y + y);
        }
    }
}

int main() {
    float psi = 0, theta = 0, phi = 0;
    float increment = M_PI / 180 * 10;
    int theta_mul = 1;
    float width = 10;
    clear_zbuffer();
    

    while (1) {
        // calculate cube
        set_buffer_background('.');
        clear_zbuffer();
        place_cube_in_z_buffer_rotation(30, 15, 0, width, psi, theta, phi);

        // draw cube
        clear_screen();
        set_cursor_top();
        draw_buffer();

        // sleep
        // psi += increment;
        // theta += increment * theta_mul;
        // if (theta > M_PI / 2) {
        //     theta_mul = -1;
        // }
        // else if (theta < -M_PI / 2) {
        //     theta_mul = 1;
        // }

        phi += increment;
        Sleep(100);

    }
}