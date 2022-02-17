
illigal_file_name_characters = ["/", ":", "*", "?", "<", ">", "|", ".", ","]

def create_diagram_file(text):
    while True:
        try:
            diagram_file_name = input(text)

            if not isinstance(diagram_file_name, str):
                print("Filename must be a string.")
        
            elif any(character in diagram_file_name for character in illigal_file_name_characters):
                for i in illigal_file_name_characters:
                    if i in diagram_file_name:
                        print("Filename can not contain \"{}\"".format(i))
                continue

            try:
                f = open(diagram_file_name, "x")
                break
            except:
                print("File already exists.")
                
        except ValueError:
            print("Sorry, I didn't understand that.")

def read():
    pass

def write(input):
    pass

def create_class(attributes, methods):
    pass

def create_association (type_of_association, from_class, to_class):
    pass

def main():
    create_diagram_file("Enter file name: ")
    print("Do stuff")

main()  # run main