#   Algorithm To Brute Force Solve Countdown 
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

#   Converts 1 n size set to (up to) n! n-1 sets with history
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

print(solve(([1,2,3,4,25,100],""), 142))