files = ['result_log', 'result_log2', 'result_log3', 'result_log4', 'result_log_zero', 'zellze_log']

paths = {}

for filename in files:
    f = open('logs/' + filename, 'r')
    data = f.readlines()
    data = data[::2]
    data = [line.strip().split('\t') for line in data]

    for datum in data:
        problem_no = int(datum[0])
        path = datum[1].strip()
        length = float(datum[2])
        
        if problem_no in paths:
            paths[problem_no].append((path, length))
        else:
            paths[problem_no] = [(path, length)]

out_file = open('zellze.out', 'w')
validate = open('v_scores', 'w')

for i in range(495):
    problem_no = i + 1
    if problem_no in paths:
        best_path = min(paths[problem_no], key = lambda x: x[1])
        out_file.write(best_path[0])
        validate.write(str(int(best_path[1])))
        validate.write('\n')
        out_file.write('\n')
    else:
        print "%i does not have a path!" %problem_no
        out_file.write('no path\n')


