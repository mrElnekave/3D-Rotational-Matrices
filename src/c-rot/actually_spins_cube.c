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





// def get_x(x, y, z, roll, pitch, yaw):
//     return cos(pitch) * cos(yaw) * x  +  (-sin(pitch) * cos(roll) + cos(pitch) * sin(yaw) * sin(roll)) * y  +  (-sin(pitch) * -sin(roll) + cos(pitch) * sin(yaw) * cos(roll)) * z
// def get_y(x, y, z, roll, pitch, yaw):
//     return sin(pitch) * cos(yaw) * x  +  (cos(pitch) * cos(roll) + sin(pitch) * sin(yaw) * sin(roll)) * y  +  (cos(pitch) * -sin(roll) + sin(pitch) * sin(yaw) * cos(roll)) * z
// def get_z(x, y, z, roll, pitch, yaw):
//     return -sin(yaw) * x  +  (cos(yaw) * sin(roll)) * y  +  (cos(yaw) * cos(roll)) * z

float get_x(float x, float y, float z, float roll, float pitch, float yaw) {
    return cos(pitch) * cos(yaw) * x  +  (-sin(pitch) * cos(roll) + cos(pitch) * sin(yaw) * sin(roll)) * y  +  (-sin(pitch) * -sin(roll) + cos(pitch) * sin(yaw) * cos(roll)) * z;
}
float get_y(float x, float y, float z, float roll, float pitch, float yaw) {
    return sin(pitch) * cos(yaw) * x  +  (cos(pitch) * cos(roll) + sin(pitch) * sin(yaw) * sin(roll)) * y  +  (cos(pitch) * -sin(roll) + sin(pitch) * sin(yaw) * cos(roll)) * z;
}
float get_z(float x, float y, float z, float roll, float pitch, float yaw) {
    return -sin(yaw) * x  +  (cos(yaw) * sin(roll)) * y  +  (cos(yaw) * cos(roll)) * z;
}

void place_cube_in_z_buffer_rotation(float center_x, float center_y, float center_z, float width, float roll, float pitch, float yaw) {
    float x, y, z;
    for (float i = -width; i < width; i+=.5) {
        for (float j = -width; j < width; j+=.5) {
        //     perms = ((_x, _y, depth, rb.Color.blue.lighter(10)), 
        //     (_x, _y, -depth, rb.Color.blue.darker(10)), 
        //     (_x, depth, _y, rb.Color.red.lighter(10)), 
        //     (_x, -depth, _y, rb.Color.red.darker(10)), 
        //     (depth, _x, _y, rb.Color.green.lighter(10)), 
        //     (-depth, _x, _y, rb.Color.green.darker(10)))
            // Front face
            x = get_x(i, j, width, roll, pitch, yaw);
            y = get_y(i, j, width, roll, pitch, yaw);
            z = get_z(i, j, width, roll, pitch, yaw);
            final_zbuffer_logic('F', z + center_z, center_x + x, center_y + y);

            // Back face
            x = get_x(i, j, -width, roll, pitch, yaw);
            y = get_y(i, j, -width, roll, pitch, yaw);
            z = get_z(i, j, -width, roll, pitch, yaw);
            final_zbuffer_logic('B', z + center_z, center_x + x, center_y + y);

            // Left face
            x = get_x(-width, i, j, roll, pitch, yaw);
            y = get_y(-width, i, j, roll, pitch, yaw);
            z = get_z(-width, i, j, roll, pitch, yaw);
            final_zbuffer_logic('L', z + center_z, center_x + x, center_y + y);

            // Right face
            x = get_x(width, i, j, roll, pitch, yaw);
            y = get_y(width, i, j, roll, pitch, yaw);
            z = get_z(width, i, j, roll, pitch, yaw);
            final_zbuffer_logic('R', z + center_z, center_x + x, center_y + y);

            // Top face
            x = get_x(i, width, j, roll, pitch, yaw);
            y = get_y(i, width, j, roll, pitch, yaw);
            z = get_z(i, width, j, roll, pitch, yaw);
            final_zbuffer_logic('T', z + center_z, center_x + x, center_y + y);

            // Bottom face
            x = get_x(i, -width, j, roll, pitch, yaw);
            y = get_y(i, -width, j, roll, pitch, yaw);
            z = get_z(i, -width, j, roll, pitch, yaw);
            final_zbuffer_logic('O', z + center_z, center_x + x, center_y + y);

        }
    }
}

int main() {
    float roll = 0, pitch = 0, yaw = 0;
    float increment = M_PI / 180 * 3;
    int theta_mul = 1;
    float width = 10;
    clear_zbuffer();
    

    while (1) {
        // calculate cube
        set_buffer_background('.');
        clear_zbuffer();
        place_cube_in_z_buffer_rotation(60, 15, 20, width, roll, pitch, yaw);


        // draw cube
        set_cursor_top();
        clear_screen();
        set_cursor_top();
        draw_buffer();

        // sleep
        pitch += increment;
        yaw += increment * 3;
        roll += increment * 2;
        Sleep(50);

    }
}