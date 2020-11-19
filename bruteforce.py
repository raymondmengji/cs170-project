import random
import sys

def calcHappiness(rooms, happiness):
	totalHappiness = 0
	for room in rooms:
		room = list(room)
		room.sort()
		for i in range(len(room)):
			for j in range(i+1, len(room)):
				totalHappiness += happiness[room[i]][room[j]]
	return totalHappiness

def calcStress(rooms, stress):
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

#algorithm from https://codereview.stackexchange.com/questions/1526/
#by Gregory Morse, Apr 10
def subsets_k(collection, k): 
    yield from partition_k(collection, k, k)
def partition_k(collection, min, k):
  if len(collection) == 1:
    yield [ collection ]
    return

  first = collection[0]
  for smaller in partition_k(collection[1:], min - 1, k):
    if len(smaller) > k: continue
    # insert `first` in each of the subpartition's subsets
    if len(smaller) >= min:
      for n, subset in enumerate(smaller):
        yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
    # put `first` in its own subset 
    if len(smaller) < k: yield [ [ first ] ] + smaller


def bruteforce(happiness, stress, n, s_max):
    # possible number of breakout rooms:
    breakout_rooms = list(range(1, n+1))

    # corresponding max stress limit in each room:
    stress_limit = [s_max / num_room for num_room in breakout_rooms]

    s = list(range(n))
    maxHappiness = 0
    optimalRoom = None
    optimalRoomStress = None
    count = 0
    max_answers = {}
    
    for i in range(len(breakout_rooms)):
        for p in subsets_k(s, breakout_rooms[i]):
            count += 1
            rooms = p
            totalHappiness = calcHappiness(rooms, happiness)
            totalStress = calcStress(rooms, stress)

            # check if room partition is valid
            is_valid = True

            for stress_num in totalStress:
                if stress_num > stress_limit[i]:
                    is_valid = False
                    break
            if is_valid:
                try:
                    max_answers[totalHappiness] += 1
                except:
                    max_answers[totalHappiness] = 1
                    if totalHappiness >= maxHappiness:
                        maxHappiness = totalHappiness
                        optimalRoomStress = totalStress
                        optimalRoom = rooms
    optimalRoom.sort(key=lambda room: room[0]) #sort by # of first person in room
    return optimalRoom, maxHappiness
