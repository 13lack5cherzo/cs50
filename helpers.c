#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //  iterate through all rows
    for (int h1 = 0; h1 < height; h1++)
    {
        // iterate through all columns
        for (int w1 = 0; w1 < width; w1++)
        {
            // take average to get greyscale
            int gs_ave = (image[h1][w1].rgbtBlue + image[h1][w1].rgbtGreen + image[h1][w1].rgbtRed) / 3;

            // cap at 255
            if (gs_ave > 255)
            {
                gs_ave = 255;
            }

            // assign to object
            image[h1][w1].rgbtBlue = gs_ave;
            image[h1][w1].rgbtGreen = gs_ave;
            image[h1][w1].rgbtRed = gs_ave;
        }
    }
    return;
}



// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h1 = 0; h1 < height; h1++)
    {
        for (int w1 = 0; w1 < width; w1++)
        {
            // compute sepia
            int r1 = round(.393 * image[h1][w1].rgbtRed + .769 * image[h1][w1].rgbtGreen + .189 * image[h1][w1].rgbtBlue);
            int g1 = round(.349 * image[h1][w1].rgbtRed + .686 * image[h1][w1].rgbtGreen + .168 * image[h1][w1].rgbtBlue);
            int b1 = round(.272 * image[h1][w1].rgbtRed + .534 * image[h1][w1].rgbtGreen + .131 * image[h1][w1].rgbtBlue);

            // cap at 255
            if (b1 > 255)
            {
                b1 = 255;
            }
            if (g1 > 255)
            {
                g1 = 255;
            }
            if (r1 > 255)
            {
                r1 = 255;
            }

            // assign to object
            image[h1][w1].rgbtBlue = b1;
            image[h1][w1].rgbtGreen = g1;
            image[h1][w1].rgbtRed = r1;
        }
    }

    return;
}


// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // declare swapped image
    RGBTRIPLE simage[height][width];

    // create swapped image
    // iterate through all rows
    for (int h1 = 0; h1 < height; h1++)
    {
        // iterate through all columns
        for (int w1 = 0; w1 < width; w1++)
        {
            // assign to object
            simage[h1][width - w1 - 1].rgbtBlue = image[h1][w1].rgbtBlue;
            simage[h1][width - w1 - 1].rgbtGreen = image[h1][w1].rgbtGreen;
            simage[h1][width - w1 - 1].rgbtRed = image[h1][w1].rgbtRed;
        }
    }

    // replace original image with swapped one
    // iterate through all rows
    for (int h1 = 0; h1 < height; h1++)
    {
        // iterate through all columns
        for (int w1 = 0; w1 < width; w1++)
        {
            // assign to object
            image[h1][w1].rgbtBlue = simage[h1][w1].rgbtBlue;
            image[h1][w1].rgbtGreen = simage[h1][w1].rgbtGreen;
            image[h1][w1].rgbtRed = simage[h1][w1].rgbtRed;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // declare blurred image
    RGBTRIPLE simage[height][width];

    // create blurred image
    // iterate through all non-edge rows
    for (int h1 = 1; h1 < height - 1; h1++)
    {
        // iterate through all non-edge columns
        for (int w1 = 1; w1 < width - 1; w1++)
        {
            // compute blur by taking average
            int r1 = round((image[h1+1][w1].rgbtRed + image[h1+1][w1+1].rgbtRed + image[h1][w1+1].rgbtRed + image[h1-1][w1+1].rgbtRed + image[h1-1][w1].rgbtRed + image[h1-1][w1-1].rgbtRed + image[h1][w1-1].rgbtRed + image[h1+1][w1-1].rgbtRed) / 8);
            int g1 = round((image[h1+1][w1].rgbtGreen + image[h1+1][w1+1].rgbtGreen + image[h1][w1+1].rgbtGreen + image[h1-1][w1+1].rgbtGreen + image[h1-1][w1].rgbtGreen + image[h1-1][w1-1].rgbtGreen + image[h1][w1-1].rgbtGreen + image[h1+1][w1-1].rgbtGreen) / 8);
            int b1 = round((image[h1+1][w1].rgbtBlue + image[h1+1][w1+1].rgbtBlue + image[h1][w1+1].rgbtBlue + image[h1-1][w1+1].rgbtBlue + image[h1-1][w1].rgbtBlue + image[h1-1][w1-1].rgbtBlue + image[h1][w1-1].rgbtBlue + image[h1+1][w1-1].rgbtBlue) / 8);

            // cap at 255
            if (b1 > 255)
            {
                b1 = 255;
            }
            if (g1 > 255)
            {
                g1 = 255;
            }
            if (r1 > 255)
            {
                r1 = 255;
            }

            simage[h1][w1].rgbtBlue = b1;
            simage[h1][w1].rgbtGreen = g1;
            simage[h1][w1].rgbtRed = r1;
        }
    }

    // iterate through bottom row, excluding corners
    int h0 = height - 1;
    for (int w1 = 1; w1 < width - 1; w1++)
    {
        // compute blur by taking average
        int r1 = round((image[h0][w1+1].rgbtRed + image[h0-1][w1+1].rgbtRed + image[h0-1][w1].rgbtRed + image[h0-1][w1-1].rgbtRed + image[h0][w1-1].rgbtRed) / 5);
        int g1 = round((image[h0][w1+1].rgbtGreen + image[h0-1][w1+1].rgbtGreen + image[h0-1][w1].rgbtGreen + image[h0-1][w1-1].rgbtGreen + image[h0][w1-1].rgbtGreen) / 5);
        int b1 = round((image[h0][w1+1].rgbtBlue + image[h0-1][w1+1].rgbtBlue + image[h0-1][w1].rgbtBlue + image[h0-1][w1-1].rgbtBlue + image[h0][w1-1].rgbtBlue) / 5);

        // cap at 255
        if (b1 > 255)
        {
            b1 = 255;
        }
        if (g1 > 255)
        {
            g1 = 255;
        }
        if (r1 > 255)
        {
            r1 = 255;
        }

        simage[h0][w1].rgbtBlue = b1;
        simage[h0][w1].rgbtGreen = g1;
        simage[h0][w1].rgbtRed = r1;
    }

    // iterate through top row, excluding corners
    h0 = 0;
    for (int w1 = 1; w1 < width - 1; w1++)
    {
        // compute blur by taking average
        int r1 = round((image[h0+1][w1].rgbtRed + image[h0+1][w1+1].rgbtRed + image[h0][w1+1].rgbtRed + image[h0][w1-1].rgbtRed + image[h0+1][w1-1].rgbtRed) / 5);
        int g1 = round((image[h0+1][w1].rgbtGreen + image[h0+1][w1+1].rgbtGreen + image[h0][w1+1].rgbtGreen + image[h0][w1-1].rgbtGreen + image[h0+1][w1-1].rgbtGreen) / 5);
        int b1 = round((image[h0+1][w1].rgbtBlue + image[h0+1][w1+1].rgbtBlue + image[h0][w1+1].rgbtBlue + image[h0][w1-1].rgbtBlue + image[h0+1][w1-1].rgbtBlue) / 5);

        // cap at 255
        if (b1 > 255)
        {
            b1 = 255;
        }
        if (g1 > 255)
        {
            g1 = 255;
        }
        if (r1 > 255)
        {
            r1 = 255;
        }

        simage[h0][w1].rgbtBlue = b1;
        simage[h0][w1].rgbtGreen = g1;
        simage[h0][w1].rgbtRed = r1;
    }

    // iterate through left column, excluding corners
    int w0 = 0;
    for (int h1 = 1; h1 < height - 1; h1++)
    {
        // compute blur by taking average
        int r1 = round((image[h1+1][w0].rgbtRed + image[h1+1][w0+1].rgbtRed + image[h1][w0+1].rgbtRed + image[h1-1][w0+1].rgbtRed + image[h1-1][w0].rgbtRed) / 5);
        int g1 = round((image[h1+1][w0].rgbtGreen + image[h1+1][w0+1].rgbtGreen + image[h1][w0+1].rgbtGreen + image[h1-1][w0+1].rgbtGreen + image[h1-1][w0].rgbtGreen) / 5);
        int b1 = round((image[h1+1][w0].rgbtBlue + image[h1+1][w0+1].rgbtBlue + image[h1][w0+1].rgbtBlue + image[h1-1][w0+1].rgbtBlue + image[h1-1][w0].rgbtBlue) / 5);

        // cap at 255
        if (b1 > 255)
        {
            b1 = 255;
        }
        if (g1 > 255)
        {
            g1 = 255;
        }
        if (r1 > 255)
        {
            r1 = 255;
        }

        simage[h1][w0].rgbtBlue = b1;
        simage[h1][w0].rgbtGreen = g1;
        simage[h1][w0].rgbtRed = r1;
    }


    // iterate through right column, excluding corners
    w0 = width - 1;
    for (int h1 = 1; h1 < height - 1; h1++)
    {
        // compute blur by taking average
        int r1 = round((image[h1+1][w0].rgbtRed + image[h1-1][w0].rgbtRed + image[h1-1][w0-1].rgbtRed + image[h1][w0-1].rgbtRed + image[h1+1][w0-1].rgbtRed) / 5);
        int g1 = round((image[h1+1][w0].rgbtGreen + image[h1-1][w0].rgbtGreen + image[h1-1][w0-1].rgbtGreen + image[h1][w0-1].rgbtGreen + image[h1+1][w0-1].rgbtGreen) / 5);
        int b1 = round((image[h1+1][w0].rgbtBlue + image[h1-1][w0].rgbtBlue + image[h1-1][w0-1].rgbtBlue + image[h1][w0-1].rgbtBlue + image[h1+1][w0-1].rgbtBlue) / 5);

        // cap at 255
        if (b1 > 255)
        {
            b1 = 255;
        }
        if (g1 > 255)
        {
            g1 = 255;
        }
        if (r1 > 255)
        {
            r1 = 255;
        }

        simage[h1][w0].rgbtBlue = b1;
        simage[h1][w0].rgbtGreen = g1;
        simage[h1][w0].rgbtRed = r1;
    }

    // bottom left corner
    h0 = height - 1;
    w0 = 0;
    simage[h0][w0].rgbtRed = round((image[h0][w0+1].rgbtRed + image[h0-1][w0+1].rgbtRed + image[h0-1][w0].rgbtRed) / 3);
    simage[h0][w0].rgbtGreen = round((image[h0][w0+1].rgbtGreen + image[h0-1][w0+1].rgbtGreen + image[h0-1][w0].rgbtGreen) / 3);
    simage[h0][w0].rgbtBlue = round((image[h0][w0+1].rgbtBlue + image[h0-1][w0+1].rgbtBlue + image[h0-1][w0].rgbtBlue) / 3);

    // bottom right corner
    h0 = height - 1;
    w0 = width - 1;
    simage[h0][w0].rgbtRed  = round((image[h0-1][w0].rgbtRed + image[h0-1][w0-1].rgbtRed + image[h0][w0-1].rgbtRed) / 3);
    simage[h0][w0].rgbtGreen = round((image[h0-1][w0].rgbtGreen + image[h0-1][w0-1].rgbtGreen + image[h0][w0-1].rgbtGreen) / 3);
    simage[h0][w0].rgbtBlue = round((image[h0-1][w0].rgbtBlue + image[h0-1][w0-1].rgbtBlue + image[h0][w0-1].rgbtBlue) / 3);


    // top left corner
    h0 = 0;
    w0 = 0;
    simage[h0][w0].rgbtRed  = round((image[h0+1][w0].rgbtRed + image[h0+1][w0+1].rgbtRed + image[h0][w0+1].rgbtRed) / 3);
    simage[h0][w0].rgbtGreen = round((image[h0+1][w0].rgbtGreen + image[h0+1][w0+1].rgbtGreen + image[h0][w0+1].rgbtGreen) / 3);
    simage[h0][w0].rgbtBlue = round((image[h0+1][w0].rgbtBlue + image[h0+1][w0+1].rgbtBlue + image[h0][w0+1].rgbtBlue) / 3);


    // top right corner
    h0 = 0;
    w0 = width - 1;
    simage[h0][w0].rgbtRed  = round((image[h0+1][w0].rgbtRed + image[h0][w0-1].rgbtRed + image[h0+1][w0-1].rgbtRed) / 3);
    simage[h0][w0].rgbtGreen = round((image[h0+1][w0].rgbtGreen + image[h0][w0-1].rgbtGreen + image[h0+1][w0-1].rgbtGreen) / 3);
    simage[h0][w0].rgbtBlue = round((image[h0+1][w0].rgbtBlue + image[h0][w0-1].rgbtBlue + image[h0+1][w0-1].rgbtBlue) / 3);


    // replace original image with swapped one
    // iterate through all rows
    for (int h1 = 0; h1 < height; h1++)
    {
        // iterate through all columns
        for (int w1 = 0; w1 < width; w1++)
        {
            // assign to object
            image[h1][w1].rgbtBlue = simage[h1][w1].rgbtBlue;
            image[h1][w1].rgbtGreen = simage[h1][w1].rgbtGreen;
            image[h1][w1].rgbtRed = simage[h1][w1].rgbtRed;
        }
    }


    return;
}
