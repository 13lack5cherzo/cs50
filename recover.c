#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Check usage
    if (argc != 2)
    {
        return 1;
    }

    // Open file
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        printf("Could not open file.\n");
        return 1;
    }


    int file_num = 0; // file number
    FILE *output = NULL; // output pointer
    char file_name[7]; // filename
    uint8_t chunk[512]; // 512 data chunk
    int chunk_num = 0; // chunk number

    while(
        fread(&chunk, sizeof(chunk), 1, file) == 1
        )
        {
            // printf("read chunk %i\n", chunk_num);
            // chunk_num += 1;

            // Check first 4 bytes
            if (
                (chunk[0] == 0xff)
                && (chunk[1] == 0xd8)
                && (chunk[2] == 0xff)
                && ((chunk[3] & 0xf0) == 0xe0)
                )
            {
                // //
                // if after the first file, close file
                // //
                if (file_num > 0)
                {
                    fclose(output);
                }

                // //
                // generate file name
                // //
                sprintf(file_name, "%03i.jpg", file_num);
                printf("%s\n", file_name); // debug


                // //
                // open file to write to
                // //
                output = fopen(file_name, "w");
                if (output == NULL)
                {
                    printf("Could not open file.\n");
                    return 1;
                }

                // add one to file number counter
                file_num = file_num + 1;

            // //
            // write to output file
            // //

            if (file_num > 0)
            {
                fwrite(&chunk, sizeof(chunk), 1, output);
            }


            }
        }

    // Close file
    fclose(file);
    fclose(output);
}



