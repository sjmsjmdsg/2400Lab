import csv
import sys
import os


# load input contents from user
def user_input():
    # you can change the path here or use [-p <path>] <command>
    path = r'./data/basics.csv'
    input_list = sys.argv[1:]
    sys.argv[1:] = ''
    if len(input_list) == 0:
        while len(input_list) == 0:
            input_list = input("Please input the commmand:\n").strip().split()
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
    while True:
        # load the commands
        _input, path = user_input()

        if _input == 'exit':
            return

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
            fd_flag = 1
            for one_line in csv_reader:
                _key = ''
                _value = ''
                for one_element in determinant_list:
                    _key = _key + ',' + one_line[int(one_element.strip()) - 1]
                for one_element in dependent_list:
                    _value = _value + ',' + one_line[int(one_element.strip()) - 1]
                if data.get(_key) is None:
                    data[_key] = _value
                else:
                    if data[_key] != _value:
                        print("False")
                        print("The determinant is:")
                        for _id, one_element in enumerate(determinant_list):
                            if _id != 0:
                                print(end=',')
                            print(one_line[int(one_element.strip()) - 1], end='')
                        print("\nThe different elements are:")
                        print(data[_key].strip(','))
                        for _id, one_element in enumerate(dependent_list):
                            if _id != 0:
                                print(end=',')
                            print(one_line[int(one_element.strip()) - 1], end='')
                        print('\n')
                        fd_flag = 0
                        break
            if fd_flag:
                print('True')


if __name__ == '__main__':
    main()