def findLongestPalindromicString(text):
    N = len(text)
    if N == 0:
        return
    N = 2 * N + 1  # Position count
    L = [0] * N
    L[0] = 0
    L[1] = 1
    C = 1  # centerPosition
    R = 2  # centerRightPosition
    maxLPSLength = 0
    maxLPSCenterPosition = 0

    # Uncomment it to print LPS Length array
    # printf("%d %d ", L[0], L[1]);
    for i in range(2, N):

        # get currentLeftPosition iMirror for currentRightPosition i
        iMirror = 2 * C - i
        L[i] = 0
        diff = R - i
        # If currentRightPosition i is within centerRightPosition R
        if diff > 0:
            L[i] = min(L[iMirror], diff)

        # Attempt to expand palindrome centered at currentRightPosition i
        # Here for odd positions, we compare characters and
        # if match then increment LPS Length by ONE
        # If even position, we just increment LPS by ONE without
        # any character comparison
        try:
            while ((i + L[i]) < N and (i - L[i]) > 0) and (((i + L[i] + 1) % 2 == 0) or (text[(i + L[i] + 1) // 2] == text[(i - L[i] - 1) // 2])):
                L[i] += 1
        except Exception as e:
            pass

        if L[i] > maxLPSLength:  # Track maxLPSLength
            maxLPSLength = L[i]
            maxLPSCenterPosition = i

        # If palindrome centered at currentRightPosition i
        # expand beyond centerRightPosition R,
        # adjust centerPosition C based on expanded palindrome.
        if i + L[i] > R:
            C = i
            R = i + L[i]

    # Uncomment it to print LPS Length array
    print(L)
    start = (maxLPSCenterPosition - maxLPSLength) // 2
    end = start + maxLPSLength - 1
    print("LPS of string is " + text + " : ", text[start:end + 1])


# Driver program
text1 = "aa"
findLongestPalindromicString(text1)