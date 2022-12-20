

if __name__=="__main__":
    test = [(0, 1), (0, 0), (0, 1), (0, 2)]
    pointIdx = test.index((0, 0))
    print(pointIdx)
    test1 = test[:pointIdx]
    test2 = test[pointIdx + 1:]
    print(test1)
    print(test2)