from functions.write_file import write_file

def main():
    print("Writing to lorem.txt:")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    
    print("Writing to pkg/morelorem.txt:")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    
    print("Writing to /tmp/text.txt")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    
if __name__ == "__main__":
    main()
