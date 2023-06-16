
def main(n):
    numList = [[1], [1, 1]]
    for i in range(n):
       if i > 1:
            nl2 = [1]
            for j in range(len(numList[i-1])-1):
                if j < len(numList[i-1])-1:
                    a1 = numList[i-1][j] + numList[i-1][j+1]
                    nl2.append(a1)
                elif i % 2 != 0:
                    a2 = numList[i-1][j-1] + numList[i-1][j]
                    nl2.append(a2)
            print(i, nl2)
            nl2.append(1)
            numList.append(nl2)
    return numList
def tes1t(n):
    aa = n
    while True:
        while True:
            sum = 0
            for str1 in str(aa):
                sum = sum + int(str1)*int(str1)
            if sum == 1:
                return True
            else:
                print(aa)
                aa = sum
                break
        if len(str(aa)) == 1:
            # print(aa)
            return False
        else:
            pass
if __name__ == '__main__':
    numRows = int(input("请输入数字："))
    resulf1 = tes1t(numRows)
    print(resulf1)