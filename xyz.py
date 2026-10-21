array = list(map(int,input("Enter num : ").split()))
target = int (input("Enter target : "))
for i in range(len(array)):
    for j in range(i+1,len(array)):
        if array[i] + array[j] == target:
            print([i],[j])