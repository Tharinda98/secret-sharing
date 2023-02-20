import time

letters=[" ","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
message="HELLO WORLD"

words=message.strip()

for word in words:
    for c in word:
        print(c)
        count=letters.index(c)+1
        for i in range(count):
            print("flash on")
            #wait for 0.5 sec
            time.sleep(0.5)
            print("flash off")
            #wait for 0.5 sec
            time.sleep(0.5)
        time.sleep(1)
    