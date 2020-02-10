from tests.utils import dump_output



def load_data(filename):
    result = []
    with open(filename, 'r') as csv_in:
        header = None
        for line in csv_in.readlines():
            parts = line.split(',')
            if header is None:
                header = parts
            else:
                item = dict()
                for i, column in enumerate(header):
                    item[column] = parts[i]
                result.append(item)
    return result


data = load_data('./conditional.csv')
gender_column = [x['gender'] for x in data]
for gender in set(gender_column):
    print(f'Gender: {gender} has {len([x for x in gender_column if x == gender])}')
