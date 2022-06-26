import os
from helper_LSB import LSB

LSB_obj = LSB()


def main():
    select = input("Enccoding (E) || Decoding (D) : ")
    if select == 'E':
        # remove clutters
        if os.path.exists("./generated-data/out.txt"):
            os.remove("./generated-data/out.txt")
        if os.path.exists("./generated-data/pls.txt.enc"):
            os.remove("./generated-data/pls.txt.enc")
        if os.path.exists("./generated-data/pls.txt"):
            os.remove("./generated-data/pls.txt")
        if os.path.exists("./images/output.png"):
            os.remove("./images/output.png")

        if os.path.exists("./images/input.png"):
            secretMessage = input("Enter the secret message : ")
            LSB_obj.LSB_Encoding(secretMessage)
            if os.path.exists("./generated-data/pls.txt"):
                os.remove("./generated-data/pls.txt")
        else:
            print("error: image is not present")

    if select == 'D':
        if os.path.exists("./generated-data/pls.txt.enc"):
            decodedText = LSB_obj.LSB_Decoding()
            print(decodedText)
        else:
            print("error: PLS file was not found")
        pass


main()
