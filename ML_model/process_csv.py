import csv

if __name__ == '__main__':
    with open('reworked_dataset.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        with open('datasets/Data v1 t9 without lvl.csv') as f:
            lis = [line.split('\n') for line in f]
            # print(lis)
            # print(lis[0])
            rows = []
            for i in range(0, len(lis)):
                rows.append(lis[i][0])
            for i in range(0, len(rows)):
                rows[i] = rows[i].split(',')
                for j in range(0, len(rows[i])):
                    rows[i][j] = rows[i][j][:5]
                    s = ','
                    mylist = (s.join(rows[i]))
                    print(mylist)
                    print(len(mylist))
                    print(type(mylist))
                wr.writerow(rows[i])
