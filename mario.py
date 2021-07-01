
if __name__ == "__main__":


    height = int(input("Height: "))
    if ~(height > 0):
        height = int(input("Height: "))


    for col1 in range (1, height + 1):
        print(" " * (height - col1) + "#" * col1)



