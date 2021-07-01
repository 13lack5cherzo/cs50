
def get_height():
    """function to get height from user"""
    try:
        height = int(input("Height: "))
    except:
        height = -1
    return height

if __name__ == "__main__":

    height = get_height()

    # check
    while not ((height > 0) & (height < 9)):
        height = get_height()


    for col1 in range (1, height + 1):
        print(" " * (height - col1) + "#" * col1)



