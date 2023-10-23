class box:
    #box is the unit in the grid
    def __init__(self,r):
        self.reward = r
        self.utility = 0
        self.prevUtility = 0
        self.north= self
        self.east= self
        self.south= self
        self.west= self
        self.policy = 'stay'

    def get_state_utility(self,p,disc,t):
        #get_state_utility method
        if (self.north == self or self.north == t):
            nr = 0
        else:
            nr = self.north.reward
        if (self.east == self or self.east == t):
            er = 0
        else:
            er = self.east.reward
        if (self.south == self or self.south == t):
            sr = 0
        else:
            sr = self.south.reward
        if (self.west == self or self.west == t):
            wr = 0
        else:
            wr = self.west.reward

        North = p * (disc*self.north.prevUtility + nr) + ((1-p)/2)*(self.east.prevUtility + er) + ((1-p)/2)*(self.west.prevUtility + wr)
        East = p * (disc * self.east.prevUtility + er) + ((1-p)/2)* (self.north.prevUtility + nr) + ((1-p)/2)* (self.south.prevUtility + sr)
        West = p * (disc * self.west.prevUtility + wr) + ((1-p)/2)* (self.north.prevUtility + nr) + ((1-p)/2)* (self.south.prevUtility + sr)
        South = p * (disc * self.south.prevUtility + sr) + ((1-p)/2)* (self.east.prevUtility + er) + ((1-p)/2)* (self.west.prevUtility + wr)
        Stay = 1*(disc*self.prevUtility)

        max_value = float("-inf")
        max_direction = None

        # Calculate values for each direction
        directions = ["North", "East", "West", "South", "Stay"]
        values = [North, East, West, South, Stay]

        for direction, value in zip(directions, values):
            if value > max_value:
                max_value = value
                max_direction = direction

        self.utility = max_value
        self.policy = max_direction

        return

def changePastUtility( listOfBoxes):
    for x in listOfBoxes:
        x.prevUtility = x.utility

def iterateValue(listOfBoxes, terminal, p, disc):
    max_diff = float("-inf")
    for x in listOfBoxes:
        if x == terminal:
            continue
        else:
            x.get_state_utility(p, disc, terminal)

    for x in listOfBoxes:
        if max_diff < abs(x.utility - x.prevUtility):
            max_diff = abs(x.utility - x.prevUtility)

    changePastUtility(listOfBoxes)
    return max_diff

def connect_boxes(b1, b2, b3, b4, b5, b6):
    # Connect b1 to its neighbors
    b1.east = b2
    b1.north = b4

    # Connect b2 to its neighbors
    b2.west = b1
    b2.east = b3
    b2.north = b5

    # Connect b3 to its neighbors
    b3.north = b6
    b3.west = b2

    # Connect b4 to its neighbors
    b4.south = b1
    b4.east = b5

    # Connect b5 to its neighbors
    b5.west = b4
    b5.south = b2
    b5.east = b6

    # Connect b6 to its neighbors
    b6.west = b5
    b6.south = b3

# Input for reward values
reward_b1 = float(input("Enter reward for b1: "))
reward_b2 = float(input("Enter reward for b2: "))
reward_b3 = float(input("Enter reward for b3: "))
reward_b4 = float(input("Enter reward for b4: "))
reward_b5 = float(input("Enter reward for b5: "))
reward_b6 = float(input("Enter reward for b6: "))

#epsilon value input
epsilon = float(input("Enter reward for epsilon value to determine the convergance: "))

# Create box objects with user-provided rewards
b1 = box(reward_b1)
b2 = box(reward_b2)
b3 = box(reward_b3)
b4 = box(reward_b4)
b5 = box(reward_b5)
b6 = box(reward_b6)

# # hardcoded input
# b1,b2,b3,b4,b5,b6 = box(-0.1),box(-0.1),box(1),box(-0.1),box(-0.1),box(-0.05)
p = 0.9
gamma = 0.999


connect_boxes(b1, b2, b3, b4, b5, b6)

#predefined terminal
terminal = b3
terminal.prevUtility = 0
terminal.utility = 1

#measure of convergance
max_diff = float(1)
boxList = [b1,b2,b3,b4,b5,b6]

#iteration counter
x = 0

while max_diff>epsilon:

    x = x+1
    max_diff = iterateValue(boxList,terminal,p,gamma)

#Output
print("When converged to epsilon 0.1",x,"times looped")
for x in range(6):

    print("box:", x+1, "utility:", boxList[x].utility, "and policy:", boxList[x].policy)




