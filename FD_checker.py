import csv
import sys
import os


# load input contents from user
def user_input():
    # you can change the path here or use [-p <path>] <command>
    path = r'D:\Downloads\title.ratings.tsv\ratings.csv'
    _input = input()
    input_list = _input.strip().split()
    if len(input_list) != 3 and len(input_list) != 1:
        print('Numbers of parameters are not right')
        sys.exit()
    if len(input_list) == 3:
        if input_list[0] != '-p':
            print('Unknown option %s' % (input_list[0]))
            sys.exit()
        path = input_list[1]
    _input = input_list[-1]
    return _input, path


def main():
    # load the commands
    _input, path = user_input()

    # check the availability of path
    if not (os.path.exists(path) and os.path.isfile(path)):
        print('Error: The path does not exist or it is not a file')
        sys.exit()

    # check the correctness of commands
    try:
        determinant_list = _input.split('->')[0].split(',')
        dependent_list = _input.strip('\r\n').split('->')[1].split(',')
    except IndexError:
        print('Error: Format of command is not right')
        sys.exit()

    # read the csv file
    data = {}
    with open(path, encoding='utf-8') as file_r:
        csv_reader = csv.reader(file_r, delimiter=',')
        schema_len = len(next(csv_reader))

        # check the scale of index of determinant list
        for num in determinant_list:
            try:
                num = int(num)
            except ValueError:
                print('Error: Index out of scale')
                sys.exit()
            if num < 1 or num >schema_len:
                print('Error: Index out of scale')
                sys.exit()

        # check the scale of index of dependent list
        for num in dependent_list:
            try:
                num = int(num)
            except ValueError:
                print('Error: Index out of scale')
                sys.exit()
            if num < 1 or num >schema_len:
                print('Error: Index out of scale')
                sys.exit()

        # check functional dependencies
        for one_line in csv_reader:
            _key = ''
            _value = ''
            for one_element in determinant_list:
                _key = _key + one_line[int(one_element.strip()) - 1]
            for one_element in dependent_list:
                _value = _value + one_line[int(one_element.strip()) - 1]
            if data.get(_key) is None:
                data[_key] = _value
            else:
                if data[_key] != _value:
                    print("False")
                    return
        print('True')


if __name__ == '__main__':
    main()