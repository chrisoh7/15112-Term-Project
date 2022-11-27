# # Note: As this requires read-write access to your hard drive,
# #       this will not run in the browser in Brython.

# def readFile(path):
#     with open(path, "rt") as f:
#         return f.read()

# def writeFile(path, contents):
#     with open(path, "wt") as f:
#         f.write(contents)

# contentsToWrite = "This is a test!\nIt is only a test!"
# writeFile("foo.txt", contentsToWrite)

# contentsRead = readFile("foo.txt")
# assert(contentsRead == contentsToWrite)

# print("Open the file foo.txt and verify its contents.")

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
leaderboard = {}

recordList = readFile("leaderboard.txt").splitlines()
for elem in recordList:
    leaderboard[elem.split(",")[0]] = elem.split(",")[1]

def boardEdit(time, user = "user"):
    leaderboard[time] = user

def boardReturn():
    time = sorted(leaderboard)
    result = []
    resultString = ""
    for i in range(0, len(time)):
        resultString += f"{i+1}.    {leaderboard[time[i]]}    {time[i]}\n"
        result.append((time[i], leaderboard[time[i]]))
    return resultString

print(boardReturn())