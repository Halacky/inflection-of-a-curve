from collections import deque 

xy = [[5, 20], [3, 18], [2, 19], [1.5, 16], [5.5, 9], [4.5, 8], 
    [3.5, 12], [2.5, 11], [3.5, 3], [2, 3], [2, 6], [0, 6], 
    [2.5, -4], [4, -5], [6.5, -2], [7.5, -2.5], [7.7, -3.5], [6.5, -8]]

dq_x = deque(maxlen=5)
dq_y = deque(maxlen=5)
last_x = None
last_y = None
type_of_seq_x = None
type_of_seq_y = None

for i, point in enumerate(xy):
    x, y = point
    print(point)
    if len(dq_x) == 0:
        last_x = x
        dq_x.append(last_x)
        print(f"Init dx_x")
    else:
        if x < last_x and type_of_seq_x == -1 or x > last_x and type_of_seq_x == 1:
            print(f"Seq continue to {type_of_seq_x}")
            if len(dq_x) == 5:
                dq_x.popleft()
                print(f"Seq continue to {type_of_seq_x} and longer then 5 times")
            last_x = x
            dq_x.append(last_x)
        elif x < last_x and type_of_seq_x is None:
            last_x = x
            dq_x.append(last_x)
            type_of_seq_x = -1
            print(f"Init type of seq {type_of_seq_x}")

        elif x > last_x and type_of_seq_x is None:
            last_x = x
            dq_x.append(last_x)
            type_of_seq_x = 1
            print(f"Init type of seq {type_of_seq_x}")

        elif x > last_x and type_of_seq_x == -1 or x < last_x and type_of_seq_x == 1:
            if len(dq_x) == 5:
                print(f"Longer seq rotating from {type_of_seq_x} to {type_of_seq_x * -1}")
            else:
                print(f"Not enought seq rotating from {type_of_seq_x} to {type_of_seq_x * -1}")
            dq_x.clear()
            last_x = x
            dq_x.append(last_x)
            type_of_seq_x *= -1

    if len(dq_y) == 0:
        last_y = x
        dq_y.append(last_y)
    else:
        if x < last_y and type_of_seq_y == -1 or x > last_y and type_of_seq_y == 1:
            if len(dq_y) == 5:
                dq_y.popleft()
            last_y = x
            dq_y.append(last_y)
        elif x < last_y and type_of_seq_y is None:
            last_y = x
            dq_y.append(last_y)
            type_of_seq_y = -1
        elif x > last_y and type_of_seq_y is None:
            last_y = x
            dq_y.append(last_y)
            type_of_seq_y = 1
        elif x > last_y and type_of_seq_y == -1 or x < last_y and type_of_seq_y == 1:
            dq_y.clear()
            last_y = x
            dq_y.append(last_y)
            type_of_seq_y *= -1
