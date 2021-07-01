
if __name__ == "__main__":
    acc_num = str(input("Number: "))

    # get vendor
    vendor = "" # placeholder for vendor
    if (acc_num[0:2] in ["34", "37"]):
        vendor = "AMEX\n"
    elif (acc_num[0:2] in [str(n1) for n1 in range(51, 56)]):
        vendor = "MASTERCARD\n"
    elif (acc_num[0] == "4"):
        vendor = "VISA\n"
    else:
        vendor = "INVALID\n"

    print(vendor)




