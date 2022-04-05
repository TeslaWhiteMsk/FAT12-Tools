import sys
import fat12info
def choice():
    while(1):
        print("\ni) Print image info")
        print("f) Print files info")
        print("s) Print short files info")
        print("a) About author")
        print("e) Exit from utility")
        try:
            option=input(">")
        except:
            print("\nWrong input.")
            continue
        if option=="e":
            print("\nThanks for using FAT12 TOOLS!")
            break
        elif option=="i":
            fat12info.print_info(img_name)
            continue
        elif option=="f":
            fat12info.print_files(img_name)
            continue
        elif option=="s":
            fat12info.short_print_files(img_name)
            continue
        elif option=="a":
            print("\nFAT12 TOOLS \nby TeslaWhiteMsk \nFanzen2010@gmail.com")
            continue
        else:
            print("\nWrong input")
            continue
    return

print("FAT12 TOOLS 0.3.0") #Begin
try:
    img_name= sys.argv[1]
except IndexError:
    img_name = 'input.txt'
choice()
