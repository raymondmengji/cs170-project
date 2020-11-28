from parse import read_input_file, read_output_file
from utils import calculate_happiness
import sys

if __name__ == '__main__':
    assert len(sys.argv) == 3
    input_type = sys.argv[1]
    input_num  = int(sys.argv[2])
    input_path  = input_type + '/' + input_type + "-" + str(input_num) + '.in'
    output_path = input_type + '_outputs/' + input_type + "-" + str(input_num) + '.out'
    G, s = read_input_file(input_path, 100)
    D = read_output_file(output_path, G, s)
    print("Happiness:", calculate_happiness(D, G))
