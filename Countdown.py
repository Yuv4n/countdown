#   Yuvan Marimuthu
#   Countdown

import random
import threading
import time
import operator

stop_event = threading.Event()

def game():

    larges = [25, 50, 75, 100]
    smalls = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]

    print("You may chose 6 numbers.")
    parity, check = True, True

    #   Input sanitisation and validation
    while check == True:
        while parity:
            try:
                smallCount = int(input("How many small numbers would you like?\n"))
                parity = False
                if smallCount > 6:
                    print("Please don't chose a number greater than 6.")
                    parity = True
                elif smallCount < 0:
                    print("Please chose a positive number.")
                    parity = True
                elif smallCount < 2:
                    print("You need at least 2 small numbers.")
                    parity = True
            except ValueError:
                print("Please only input a number, by itself.")
        parity = True

        while parity:
            try:
                largeCount = int(input("How many large numbers would you like? Note, you may not chose more than 4.\n"))
                parity = False
                if largeCount > 4:
                    print("Please don't chose more than 4 large numbers")
                    parity = True
                elif largeCount < 0:
                    print("Please chose a positive number.")
                    parity = True
            except ValueError:
                print("Please only input a number, by itself.")
        parity = True

        if smallCount + largeCount != 6:
            print("Make sure you chose integers such that the number of large and small numbers sum to 6.")
        else:
            check = False

    #   Generate Number Set and Target
    nums = []
    for small in range(smallCount):
        t = random.choice(smalls)
        nums.append(t)
        smalls.remove(t)
    for large in range(largeCount):
        t = random.choice(larges)
        nums.append(t)
        larges.remove(t)
    target = random.randint(101,999)

    print(f"Your numbers are: {nums} and your target is {target}")

    difficulty = 5
    solution = {}

    #   Create threads
    solveThread = threading.Thread(target=storeSolve, args=(nums, target, solution))
    timerThread = threading.Thread(target=time.sleep, args=(difficulty,))

    #   Start threads
    solveThread.start()
    timerThread.start()
    #   End threads
    solveThread.join()
    timerThread.join()
    print("Your time has run out.")

    #   Check Answer
    result, found, score = check_(nums, target)
    print(result)
    if not found:
        if solution[0]:
            print(f"A possible correct solution for the exact answer is: {solution[0]}")
        else:
            print("No exact solution Exists")
    return score

#   Algorithm to Store Solution
def storeSolve(nums, target, solution):
    solution[0] = solve((nums, ""), target)

#   Algorithm To Brute Force Solve Countdown, Recursively 
def solve(nums, target):

    if target in nums[0]:
        return nums[1][:-2]

    if len(nums[0]) > 1:
        shorts = shrink(nums)
        for short in shorts:
            solved = solve(short, target)
            if solved:
                return solved
    return False

#   Converts 1 n size set to (up to) n! n-1 sets with history, tree grows exponentially => exponential time/space complexity
def shrink(nums):
    shortNums = []
    for i in range(len(nums[0])-1):
        for j in range(i+1, len(nums[0])):
            for count in range(6):
                shortNum = nums[0].copy()
                steps = nums[1]

                if count % 6 == 0:
                    n = nums[0][i]+nums[0][j]
                    steps += "{} + {} = {}, ".format(nums[0][i], nums[0][j], n)
                    shortNum.pop(i)
                    shortNum.pop(j-1)
                    shortNum.append(n)
                elif count % 6 == 1:
                    n = nums[0][i]*nums[0][j]
                    steps += "{} * {} = {}, ".format(nums[0][i], nums[0][j], n)
                    shortNum.pop(i)
                    shortNum.pop(j-1)
                    shortNum.append(n)
                elif count % 6 == 2:
                    n = nums[0][i]-nums[0][j]
                    steps += "{} - {} = {}, ".format(nums[0][i], nums[0][j], n)
                    shortNum.pop(i)
                    shortNum.pop(j-1)
                    shortNum.append(n)
                elif count % 6 == 3:
                    n = nums[0][j]-nums[0][i]
                    steps += "{} - {} = {}, ".format(nums[0][j], nums[0][i], n)
                    shortNum.pop(i)
                    shortNum.pop(j-1)
                    shortNum.append(n)
                elif count % 6 == 4:    
                    if  nums[0][j] == 0:
                        break
                    n = nums[0][i]/nums[0][j]
                    if str(n)[::-1][0] == "0":
                        steps += "{} / {} = {}, ".format(nums[0][i], nums[0][j], int(n))
                        shortNum.pop(i)
                        shortNum.pop(j-1)
                        shortNum.append(int(n))
                elif count % 6 == 5:    
                    if  nums[0][i] == 0:
                        break
                    n = nums[0][j]/nums[0][i]
                    if str(n)[::-1][0] == "0":
                        steps += "{} / {} = {}, ".format(nums[0][j], nums[0][i], int(n))
                        shortNum.pop(i)
                        shortNum.pop(j-1)
                        shortNum.append(int(n))
                    else:
                        break

                if all(num[0] != shortNum for num in shortNums) and shortNum != nums[0]:
                    shortNums.append((shortNum, steps))

    return shortNums

#   2 step process, ensure if input in correct form, then calculate input + score
#   Calulate result of Input, and Check if Valid

#   Desired Input Form -> "3 + 4 = 7, 7 * 2 = 14, 14 * 3 = 42"
#   Check Form of Input, then if Arithmetic is Correct

def check_(nums, target):

    # Assuming input in correct form
    operations = {
                "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv}
    valid = False

    while not valid:
        try:
            steps = input("Please enter your guess for the solution, ie the solution should be written like this, 3 + 4 = 7, 7 * 2 = 14, 14 * 3 = 42. Only using numbers from the given set or numbers made from said set.\n").split(",")
            for i in range(len(steps)):
                steps[i] = steps[i].split()
            for step in steps:
                if not step[0].isnumeric() or not step[2].isnumeric() or not step[4].isnumeric():
                    raise TypeError
                if not step[1] in operations:
                    raise TypeError
                if not step[3] == "=":
                    raise TypeError
            valid = True
        except TypeError:
            print("Please ensure your answer is entered in the same form as the example.")

    for step in steps:
        result = int(step[4])
        if (not int(step[0]) in nums or not int(step[2]) in nums):
            return "Your Equation uses numbers that aren't from the given set or numbers made from said set. Your score is 0", False, 0
        elif not int(step[4]) == operations[step[1]](int(step[0]), int(step[2])):
            return "Your Equation relies on incorrect arithmetic. Your score is 0", False, 0
        else:
            nums.remove(int(step[0]))
            nums.remove(int(step[2]))
            nums.append(int(step[4]))

    if result == target:
        return "Correct Solution Found. Congragulations your score is 10", True, 10
    else:
        score = abs(result - target)
        if score > 10:
            return "Good Try, but you're too far away. Your score is 0", False, 0
        else:
            return f"Well done. Your score is {10 - score}", False,  10 - score

game()