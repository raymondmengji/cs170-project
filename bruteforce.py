import random

def calcHappiness(rooms):
	totalHappiness = 0
	for room in rooms:
		room = list(room)
		room.sort()
		for i in range(len(room)):
			for j in range(i+1, len(room)):
				totalHappiness += happiness[room[i]][room[j]]
	return totalHappiness

def calcStress(rooms):
	arr = []
	for room in rooms:
		totalStress = 0
		room = list(room)
		room.sort()
		for i in range(len(room)):
			for j in range(i+1, len(room)):
				totalStress += stress[room[i]][room[j]]
		arr.append(totalStress)
	return arr


def sorted_k_partitions(seq, k):
    """Returns a list of all unique k-partitions of `seq`.

    Each partition is a list of parts, and each part is a tuple.

    The parts in each individual partition will be sorted in shortlex
    order (i.e., by length first, then lexicographically).

    The overall list of partitions will then be sorted by the length
    of their first part, the length of their second part, ...,
    the length of their last part, and then lexicographically.
    """
    n = len(seq)
    groups = []  # a list of lists, currently empty

    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > k - len(groups):
                for group in groups:
                    group.append(seq[i])
                    yield from generate_partitions(i + 1)
                    group.pop()

            if len(groups) < k:
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)
                groups.pop()

    result = generate_partitions(0)

    # Sort the parts in each partition in shortlex order
    result = [sorted(ps, key = lambda p: (len(p), p)) for ps in result]
    # Sort partitions by the length of each part, then lexicographically.
    result = sorted(result, key = lambda ps: (*map(len, ps), ps))

    return result

if __name__ == "__main__":
	n = 10
	s_max = random.randint(0, 100000)/1000

	happiness = {}
	for i in range(n):
		happiness[i] = {}

	for i in range(n):
		for j in range(i+1, n):
			happiness[i][j] = random.randint(0, 100000)/1000

	# happiness[0][1] = 9.2
	# happiness[0][2] = 5.4
	# happiness[0][3] = 2.123
	# happiness[1][2] = 75.4
	# happiness[1][3] = 18
	# happiness[2][3] = 87

	stress = {}
	for i in range(n):
		stress[i] = {}

	for i in range(n):
		for j in range(i+1, n):
			stress[i][j] = random.randint(0, 100000)/1000

	# stress[0][1] = 3
	# stress[0][2] = 40.8
	# stress[0][3] = 98
	# stress[1][2] = 8
	# stress[1][3] = 57.904
	# stress[2][3] = 9.4

	# possible number of breakout rooms:
	breakout_rooms = list(range(1, n+1))

	# corresponding max stress limit in each room:
	stress_limit = [s_max / num_room for num_room in breakout_rooms]


	s = list(range(n))

	maxHappiness = 0
	optimalRoom = None
	optimalRoomStress = None
	count = 0
	for i in range(len(breakout_rooms)):
		print("Stress limit per room:", stress_limit[i])
		partition = sorted_k_partitions(s, breakout_rooms[i])
		for p in partition:
			count += 1
			rooms = p
			totalHappiness = calcHappiness(rooms)
			totalStress = calcStress(rooms)
			print("Room split:", rooms, "Total Happiness:", totalHappiness, "Total Stress:", totalStress)

			# check if room partition is valid
			is_valid = True

			for stress_num in totalStress:
				if stress_num > stress_limit[i]:
					is_valid = False
			if is_valid:
				if totalHappiness > maxHappiness:
					maxHappiness = totalHappiness
					optimalRoomStress = totalStress
					optimalRoom = rooms
		print("\n")
	print("Total:", count)
	print("Optimal Room:", optimalRoom, "Max Happiness:", maxHappiness, "Stress per room:", optimalRoomStress)
		
			


		









