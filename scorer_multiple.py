import sys

# assumes output file is well formatted
# if you have errors, make sure you double check the output format 

ninstances = 495
def main(argv):
  fanswer = open("answer.out", "r")
  fout = open("score.txt", "w")
  for i in xrange(ninstances):
    finstance = open("instances/"+`i+1`+".in", "r")
    N = int(finstance.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in finstance.readline().split()]
    c = finstance.readline()
    finstance.close()

    perm = [int(x) for x in fanswer.readline().split()]
    fout.write(processCase(N, d, c, perm) + "\n")

  fout.close()
  fanswer.close()


def processCase(N, d, c, perm):
  if len(perm) != N:
    return "-1"
  v = [0] * N
  prev = 'X'
  count = 0
  for i in xrange(N):
    if v[perm[i]-1] == 1: 
      return "-1"
    v[perm[i]-1] = 1

    cur = c[perm[i]-1]
    if cur == prev:
      count += 1
    else:
      prev = cur
      count = 1

    if count > 3:
      return "-1"

  cost = 0
  for i in xrange(N-1):
    cur = perm[i]-1
    next = perm[i+1]-1

    cost += d[cur][next]

  return str(cost)

if __name__ == '__main__':
    main(sys.argv[1:])
