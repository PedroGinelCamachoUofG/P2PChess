from itertools import permutations
coordinates = 0
lst = [1,2]
combinations = list(permutations(lst))
for x in range(len(combinations)):

    print(combinations[x])
positions = []