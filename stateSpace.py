# LERRE = HANNA + 4
import matplotlib.pyplot as plt


# decrypts a ciphertext using a caesar cipher with a given shift
def decryptCeasar(ciphertext, key):
    plaintext = ""
    for c in ciphertext:
        if c.isalpha():
            if c.islower():
                plaintext += chr((ord(c) - ord('a') - key) % 26 + ord('a'))
            else:
                plaintext += chr((ord(c) - ord('A') - key) % 26 + ord('A'))
        else:
            plaintext += c
    return plaintext


# heuristic 1 - Trying all 25 keys
def stateSpace1(ciphertext):
    states = []
    for i in range(26):
        states.append(decryptCeasar(ciphertext, i))
    return states


# calculates frequency of each letter in a given text
def calcFrequency(text):
    count = {}
    for c in text:
        if c.isalpha():
            if c in count:
                count[c] += 1
            else:
                count[c] = 1
    return count


# finds the most frequent letters from a given frequency dictionary
def maxFrequency(count):
    maxF = max(count.values())
    maxFchar = [i for i, v in count.items() if v == maxF]
    return maxFchar


# heuristic 2 - most frequent letter mapped to "E"
def stateSpace2(ciphertext):
    ciphertext = ciphertext.upper()

    shifts = [ord(i) - (ord('E')) %
              26 for i in maxFrequency(calcFrequency(ciphertext))]

    states = []
    for i in shifts:
        states.append(decryptCeasar(ciphertext, i))

    return states


# calculates frequency of each trigram in a given text
def calcTrigramFreq(text):
    count = {}
    text = text.split()
    for word in text:
        if len(word) == 3:
            if word in count:
                count[word] += 1
            else:
                count[word] = 1

    return count


# finds the most frequent trigrams from a given trigram frequency dictionary
def maxFreqTrigram(count):
    if not count:
        return []
    maxF = max(count.values())
    maxFtrigram = [w for w, v in count.items() if v == maxF]
    return maxFtrigram


# checks if a trigram is a possible mapping for "THE"
def isTrigramThe(trigram):
    if ((ord('T') - ord('H')) % 26) == ((ord(trigram[0]) - ord(trigram[1])) % 26):
        if ((ord('H') - ord('E')) % 26) == ((ord(trigram[1]) - ord(trigram[2])) % 26):
            return True
    return False


# heuristic 3 - most frequent trigram mapped to "THE"
def stateSpace3(ciphertext):
    ciphertext = ciphertext.upper()
    theTrigrams = [tri for tri in maxFreqTrigram(
        calcTrigramFreq(ciphertext)) if isTrigramThe(tri)]

    shifts = [(ord(tri[0]) - ord('T')) % 26 for tri in theTrigrams]

    states = []
    for i in shifts:
        states.append(decryptCeasar(ciphertext, i))

    return states


# calculates the distance between two states
def stateDistance(a, b):
    return (ord(b[0]) - ord(a[0])) % 26


# shows state space graph for a given heuristic
def stateSpaceGraph(stateSpace, goalState, heuristic):
    x = range(len(stateSpace))
    y = [-stateDistance(state, goalState) for state in stateSpace]
    plt.xticks(x, stateSpace)
    plt.title(f"State Space Graph -  Heuristic {heuristic}")
    plt.xlabel('States')
    plt.ylabel('Heuristic Value')
    plt.plot(x, y)
    plt.show()


# main function
stateSpaceGraph(stateSpace1("lerre"), "hanna", "1")
stateSpaceGraph(stateSpace2("lerre"), "hanna", "2")
stateSpaceGraph(stateSpace3("lerre"), "hanna", "3")
