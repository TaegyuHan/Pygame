f = open("text.txt", "w")
for i in range(1, 21):
    f.write("'/image/RacingCar{0:0>2}.png',".format(i))

f.close()
