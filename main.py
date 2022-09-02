import argparse


def main():
    parser = argparse.ArgumentParser(description="Test - Bla \n Bla Bla \n 12345")

    parser.add_argument('-input', type=str, required=True, help='path to patient folder with dicom files')
    # parser.add_argument('-output', type=str, required=True, help='path to patient folder')
    # Use a breakpoint in the code line below to debug your script.

    args = parser.parse_args()
    path_input = args.input

    print(f'{path_input}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
