import operator
#   2 step process, ensure if input in correct form, then calculate input + score
#   Calulate result of Input, and Check if Valid

#   Desired Input Form -> "3 + 4 = 7, 7 * 2 = 14, 14 * 3 = 42"
#   Check Form of Input, then if Arithmetic is Correct

def check(nums, target):

    # Assuming input in correct form
    operations = {
                "+" : operator.add,
                "-" : operator.sub,
                "*" : operator.mul,
                "/" : operator.truediv}
    valid = False

    while not valid:
        try:
            steps = input("Please enter your guess for the solution,\nie the solution should be written like this, 3 + 4 = 7, 7 * 2 = 14, 14 * 3 = 42\n").split(",")
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

print(check([2,3,3,4,7,25,50],42))