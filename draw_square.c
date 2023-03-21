#include <stdio.h>
#include <Windows.h>
#define _USE_MATH_DEFINES // This is required to get M_PI
#include <math.h>



// My terminal width is 160 characters
// and I want 50 characters of height

#define TERMINAL_WIDTH 159
#define TERMINAL_HEIGHT 30

char screen_buffer[TERMINAL_HEIGHT][TERMINAL_WIDTH];
// float z_buffer[TERMINAL_HEIGHT][TERMINAL_WIDTH];

int screen_width = TERMINAL_WIDTH;
int screen_height = TERMINAL_HEIGHT;


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

void place_cube_in_buffer(int topleft_x, int topleft_y, int width, int height, char cube) {
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            screen_buffer[topleft_y + y][topleft_x + x] = cube;
        }
    }
}

void draw_buffer() {
    for (int i = 0; i < screen_height; i++) {
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
// void final_zbuffer_logic(char c, float z_val, int x, int y) {
//     if (y >= 0 && y < screen_height && x >= 0 && x < screen_width) {
//         if (z_val > z_buffer[y][x]) {
//             z_buffer[y][x] = z_val;
//             screen_buffer[y][x] = c;
//         }
//     }
// }


// make the simple cube spin using 2d rotational matrix
/**
 * @brief will rotate the cube with a 2d rotational matrix
 * 
 * @param center_x x coord of center of the cube
 * @param center_y y coord of center of the cube
 * @param width  width of the cube
 * @param height height of the cube
 * @param cube character to draw the cube with
 * @param angle angle to rotate the cube by
 */
void place_cube_in_buffer_rotation(int center_x, int center_y, int width, int height, char cube, float angle) {
    for (float x = -width; x < width; x+=.5f) {
        for (float y = -height; y < height; y+=.5f) {
            // rotate the point
            float x_rotated = x * cos(angle) - y * sin(angle);
            float y_rotated = x * sin(angle) + y * cos(angle);

            // translate the point back
            int x_translated = x_rotated + center_x;
            int y_translated = y_rotated + center_y;

            // draw the point
            screen_buffer[y_translated][x_translated] = cube;
        }
    }
}


int main() {
    float angle = 0.0f;
    float increment = M_PI / 32 ;
    while (1) {
        // calculate cube
        set_buffer_background('.');
        place_cube_in_buffer_rotation(50, 15, 10, 10, '#', angle);

        // draw cube
        set_cursor_top();
        clear_screen();
        set_cursor_top();
        draw_buffer();

        // sleep
        Sleep(125);
        angle += increment;
    }
}