import matplotlib.pyplot as plt



class Building:
    def __init__(self, l, h, r):
        self.l = l
        self.h = h
        self.r = r



class CriticalPoint:
    def __init__(self, x, h):
        self.x = x
        self.h = h


    def __repr__(self):
        return f"({self.x}, {self.h})"








# Brute Force Algorithm
# 1. Find most right x position
# 2. For every x, track max height
# 3. Extract points where hieght changes

# Time Complexity: O(n^2)
# Space Complexity: O(n)

def brute(buildings):

    # Find most right x position
    largest_x = 0
    for building in buildings:
        largest_x = max(largest_x, building.r)


    #Track max height for every x position
    heights = []
    for i in range (largest_x + 1):
        heights.append(0)

    for b in buildings:
        for i in range(b.l, b.r):
            heights[i] = max(heights[i], b.h)



    result = []
    prevHeight = 0

    for i in range(len(heights)):
        if heights[i] != prevHeight:
            result.append(CriticalPoint(i, heights[i]))
            prevHeight = heights[i]

    return result







# Merge two already computed skylines.

def merge(l, r):
    result = []
    h1 = h2 = 0
    i = j = 0

    while i < len(l) and j < len(r):
        if l[i].x < r[j].x:
            x = l[i].x
            h1 = l[i].h
            maxHeight = max(h1,h2)
            if not result or result[-1].h != maxHeight:
                result.append(CriticalPoint(x, maxHeight))
            i += 1

        elif r[j].x < l[i].x:
            x = r[j].x
            h2 = r[j].h
            maxHeight = max(h1,h2)
            if not result or result[-1].h != maxHeight:
                result.append(CriticalPoint(x, maxHeight))
            j += 1

        else:
            x = l[i].x
            h1 = l[i].h
            h2 = r[j].h
            maxHeight = max(h1,h2)
            if not result or result[-1].h != maxHeight:
                result.append(CriticalPoint(x, maxHeight))
            i += 1
            j += 1


    while i < len(l):
        result.append(l[i])
        i += 1

    while j < len(r):
        result.append(r[j])
        j += 1


    return result











# Divide and Conquer Algorithm
    # Base Case: Convert one building to two critical points
    # Divide the buildings into two halves recursively and then merge

# Time Complexity: O(nlogn)
# Space Complexity: O(n)

def divideAndConquer(buildings):
    if not buildings:
       return []

    if len(buildings) == 1:
       b = buildings[0]
       return [CriticalPoint(b.l, b.h), CriticalPoint(b.r, 0)]

    mid = len(buildings) // 2
    lSkyline = divideAndConquer(buildings[:mid])
    rSkyline = divideAndConquer(buildings[mid:])

    return merge(lSkyline, rSkyline)













# Sweep line algorithm
# Time Complexity: O(nlogn)
# Space Complexity: O(n)
def sweepLine(buildings):


    # Create events for each building, using negative height for start, possitive for end
    events = []
    for b in buildings:
        events.append((b.l, -b.h))
        events.append((b.r,b.h))


    # Sort events by x
    events.sort()

    result = []
    heights = [0]
    prev_max = 0


    for x, h in events:
        if h < 0:
            heights.append(-h)
        else:
            if h in heights:
                heights.remove(h)


        # Check current tallest building
        currentMax = max(heights)

        if currentMax != prev_max:
            result.append(CriticalPoint(x, currentMax))
            prev_max = currentMax


    return result












def visualizeSkyline(buildings, criticalPoints, title="Skyline Visualization"):
    plt.figure(figsize=(10,6))

    for b in buildings:
        x = b.l
        width = b.r - b.l
        height = b.h
        plt.bar(x, height, width=width, align='edge', color='lightblue', edgecolor='black', alpha=0.5)



    xValues = []
    yValues = []

    for i in range(len(criticalPoints)):
        cp = criticalPoints[i]
        xValues.append(cp.x)
        yValues.append(cp.h)

        if i+1 < len(criticalPoints):
            next_cp = criticalPoints[i+1]
            xValues.append(next_cp.x)
            yValues.append(cp.h)

    plt.plot(xValues, yValues, color='red', linewidth=2, label='Skyline')



    plt.xlabel("x")
    plt.ylabel("height")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()






def testCode(buildings, algorithm):

    print("Test Start")
    print(f"Algorithm: {algorithm.__name__}")

    result = algorithm(buildings)

    print("Result: ")
    for cp in result:
        print(f"({cp.x}, {cp.h})")

    visualizeSkyline(buildings, result, title=f"Skyline Visualization - {algorithm.__name__}")









if __name__ == "__main__":
    
    buildings = [
        Building(2, 10, 9),
        Building(3, 15, 7),
        Building(5, 12, 12)
    ]

    testCode(buildings, brute)
    testCode(buildings, divideAndConquer)
    testCode(buildings, sweepLine)
