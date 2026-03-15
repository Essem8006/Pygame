#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <unistd.h> // for usleep()
#include <string.h>
#include <thread>

using namespace std;

const static int npoints = 2048;
const static int fps = 100;
const static int scale = 60; //every meter is x pixles
const static int smoothing = 50;

Display *display;
int screen;
Window window;
GC gc;
unsigned long black, white;
const float volume = M_PI * pow(smoothing, 5) / 10;
const int smoothingSQ = smoothing * smoothing;

struct Vec2 {
    double x=0;
    double y=0;
};

Vec2 positions[npoints];
Vec2 velocities[npoints];

unsigned long RGB(int r, int g, int b) {
    return (r<<16) + (g<<8) + b;
}

void init() {
    display = XOpenDisplay(nullptr);
    if (!display) {
        cerr << "Failed to open X display.\n";
    }
    screen = DefaultScreen(display);
    black = BlackPixel(display, screen);
    white = WhitePixel(display, screen);

    window = XCreateSimpleWindow(display, RootWindow(display, screen), 0, 0, 800, 600, 1, white, black);//border_width bordercol and backgroundcol at end
    XSetStandardProperties(display, window, "Word", "Hi", None, NULL, 0, NULL);
    XSelectInput(display, window, ExposureMask | KeyPressMask | PointerMotionMask);// tells X server what events we want from it (ButtonPressMask | )
    gc = XCreateGC(display, window, 0, nullptr);
    XClearWindow(display, window);
    XMapRaised(display, window);
    for(int i=0;i<npoints;i++) {
        positions[i].x = rand() % 800;
        positions[i].y = rand() % 600;
    }
}

void close() {
    XFreeGC(display, gc);
    XDestroyWindow(display, window);
    XCloseDisplay(display);
    exit(0);
}

float sq(float x) {
    return x * x;
}

float density(double x, double y) {
    float density = 0;
    for(int i=0;i<npoints;i++) {
        float distance = sqrt(sq(x - positions[i].x) + sq(y - positions[i].y));
        if (distance < smoothing) {
            float influence = pow(smoothing-distance, 3);
            density += influence;
        }
    }
    return density / volume;
}

void drawDensity() {
    XWindowAttributes winAttr;
    XGetWindowAttributes(display, window, &winAttr);

    // calc densities
    vector<float> densityBuffer(winAttr.width * winAttr.height);
    fill(densityBuffer.begin(), densityBuffer.end(), 0.0f);

    for (int i = 0; i < npoints; i++) {
        int x = (int)positions[i].x;
        int y = (int)positions[i].y;

        int minx = max(0, x - smoothing);
        int maxx = min(winAttr.width, x + smoothing); // use < later on so exclubes the winAttr.width itself
        int miny = max(0, y - smoothing);
        int maxy = min(winAttr.height, y + smoothing); // same as above

        for (int y = miny; y < maxy; y++) {
            float dy = y - positions[i].y;
            float dy2 = dy * dy;
            for (int x = minx; x < maxx; x++) {
                float dx = x - positions[i].x;
                float r2 = dx * dx + dy2;

                if (r2 < smoothingSQ) {
                    float d = smoothing - sqrt(r2);
                    densityBuffer[y * winAttr.width + x] += d * d * d;
                }
            }
        }
    }
    
    XImage* img = XCreateImage(
        display,
        DefaultVisual(display, screen),
        DefaultDepth(display, screen),
        ZPixmap,
        0,
        (char*)malloc(winAttr.width * winAttr.height * 4),
        winAttr.width,
        winAttr.height,
        32,
        0
    );

    

    uint32_t* pixels = (uint32_t*)img->data;
    for (int y = 0; y < winAttr.height; ++y) {
        for (int x = 0; x < winAttr.width; ++x) {
            float d = densityBuffer[y * winAttr.width + x] / volume;

            int g = std::min((int)(10000.0f * d), 255);
            pixels[y * winAttr.width + x] = RGB(0, g, 0);
        }
    }

    XPutImage(display, window, gc, img, 0, 0, 0, 0, winAttr.width, winAttr.height);
}

void draw() {
    //XClearWindow(display, window);
    drawDensity();

    // draw particles
    XSetForeground(display, gc, white);
    XPoint points[npoints];
    for(int i=0;i<npoints;i++) {
        points[i].x = (int)positions[i].x;
        points[i].y = (int)positions[i].y;
    }
    XDrawPoints(display, window, gc, points, npoints, CoordModeOrigin);
    XFlush(display);
}

void update() {
    for(int i=0;i<npoints;i++) {
        //velocities[i].y+=scale*9.81/fps;

        positions[i].x += velocities[i].x/fps;
        positions[i].y += velocities[i].y/fps;

        if (positions[i].y > 600) {
            positions[i].y = 1200 - positions[i].y;
            velocities[i].y *= -1;
        }else if (positions[i].y < 0) {
            positions[i].y *= -1;
            velocities[i].y *= -1;
        }
        if (positions[i].x > 800) {
            positions[i].x = 1600 - positions[i].x;
            velocities[i].x *= -1;
        }else if (positions[i].x < 0) {
            positions[i].x *= -1;
            velocities[i].x *= -1;
        }
    };
    draw();
}

int main() {
    init();

    XEvent e;
    while (true) {
        // event loop
        while (XPending(display)) {
            XNextEvent(display, &e);
            if (e.type == KeyPress) {
                close();
            };
            if (e.type == Expose) draw();
            if (e.type == ButtonPress) {
                int x = e.xbutton.x, y = e.xbutton.y;
            };
            if (e.type == MotionNotify) {
                int x = e.xbutton.x, y = e.xbutton.y;
            };
        }
        update();
        usleep(1000000/fps); // 100,000 μs = 10 FPS
    }


    return 0;
}
