/*
 * (C) 2021 Sascha Hunold
 */

#include <math.h>
#include "filter.h"

const int fwidth2  = 1;
const int fheight2 = 1;

void apply_filter(png_bytep *row_pointers, int width, int height, double filter[3][3], int rounds) {    

    for(int r=0; r<rounds; r++) {        
        for(int i=fwidth2; i<width - fwidth2; i++) {        
            for(int j=fheight2; j<height - fheight2; j++) {        
                filter_on_pixel(row_pointers, i, j, filter);
            }
        }
    }

}

