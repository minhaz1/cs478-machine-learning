import random

# HW4 
# Minhaz Mahmud
GRID_SIZE = 15
NUM_ACTIONS = 4
GAMMA = .2
EPISODES = 200
DEBUG = False
NOISE = 0

def getQ(Q, state, action):
	return Q[state][action]

def getReward(state):
	# if at goal, give 100
	if state == (GRID_SIZE ** 2 - 1):
		return 100
	# otherwise 0
	return 0


def pickAction(Q, state):
	# add noise, randomly pick something
	if(random.random() < NOISE):
		return random.randint(0,3)
	
	# find max
	maxval = max(Q[state])
	actions = []
	# collect max values
	for i, item in enumerate(Q[state]):
		if item == maxval:
			actions.append(i)

	return random.choice(actions)

# get next state based on current state + action
def getNextState(state, action):
	left, right, up, down = 0, 1, 2, 3

	if action == up:
		if DEBUG:
			print "-- club going up --"
		if state < GRID_SIZE:
			return state
		else:
			return state - GRID_SIZE
	elif action == down:
		if DEBUG:
			print "-- club going down --"
		if state > (GRID_SIZE ** 2) - GRID_SIZE-1:
			return state
		else:
			return state + GRID_SIZE
	elif action == left:
		if DEBUG:
			print "-- club going left --"
		# if it's on the left edge
		if (state % GRID_SIZE) == 0:
			return state
		else:
			return state - 1
	elif action == right:
		if DEBUG:
			print "-- club going right --"
		# go right 
		if ((state+1) % GRID_SIZE) == 0:
			return state
		else:
			return state + 1

def main():
	# each state has four possible actions
	Q = [[0 for x in range(NUM_ACTIONS)] for y in range(GRID_SIZE**2)]
	current_episode = 1


	for i in range(EPISODES):
		print "Current Episode: " + str(current_episode)		
		next_state = 0
		current_state = 0
		# next action they are taking
		current_action = -1
		# while you're not at the goal
		num_steps = 0 
		while (current_state != (GRID_SIZE ** 2)-1):
			# get best action
			current_action = pickAction(Q, current_state)
			# compute next state based on best action
			next_state = getNextState(current_state, current_action)

			# set reward of current state to be instant reward of next state 
			# + the reward of the best choice of the next state
			Q[current_state][current_action] = getReward(next_state) + ((GAMMA) * Q[next_state][pickAction(Q, next_state)])
			current_state = next_state
			num_steps += 1
		current_episode += 1
		print "\tNumber of Steps: " + str(num_steps)

if __name__ == '__main__':
	main()
