f = open("c:/Users/Asus/Desktop/AI_asm02/map_space.txt","w")
i = 4
for i in range(4,21):
    f.write(str(i)+'x'+str(i)+'\n')
    for j in range(i):
        for k in range(i):
            if j == 0 or k == 0 or j == i-1 or k == i-1 :
                f.write('#')
            elif j==1 and k==1 :
                f.write('S')
            elif j==2 and k==2 :
                f.write('B')
            elif j==i-2 and k==i-2:
                f.write('T')
            else:
                f.write(' ')
        f.write('\n') 
f.close()
