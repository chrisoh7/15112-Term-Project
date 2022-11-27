def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

contentsToWrite = "00:11,Matt\n"
writeFile("leaderboard.txt", readFile("leaderboard.txt")+contentsToWrite)
contentsToWrite = "00:12,Matt\n"
writeFile("leaderboard.txt", readFile("leaderboard.txt")+contentsToWrite)
contentsToWrite = "00:13,Matt\n"
writeFile("leaderboard.txt", readFile("leaderboard.txt")+contentsToWrite)

# contentsRead = readFile("leaderboard.txt")
# assert(contentsRead == contentsToWrite)

print("Open the file foo.txt and verify its contents.")
