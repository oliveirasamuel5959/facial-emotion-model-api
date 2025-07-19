def getMinTuningOperations(queryTimes):
    # Write your code here
    num_times = 1
    repeat = 0
    
    def check_odd(queryTimes):
        bool_value = False
        for i in queryTimes:
            if i % 2 == 0:
                return False
            else:
                bool_value = True
        return bool_value
    
    is_odd = check_odd(queryTimes)
    print(is_odd)
    while not is_odd:
        print("Before: ", queryTimes)
        for i in range(len(queryTimes)):
            repeat = queryTimes.count(i)
            if queryTimes[i] % 2 == 0: # even number
                num = queryTimes[i] // 2
                queryTimes.remove(queryTimes[i])
                queryTimes.insert(i, num)
        num_times += 1
        print("After: ", queryTimes)
        is_odd = check_odd(queryTimes)
        
    return queryTimes, num_times


print(getMinTuningOperations([2, 5, 1, 6, 4, 4]))
