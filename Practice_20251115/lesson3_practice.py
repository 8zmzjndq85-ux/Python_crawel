# 練習
import random

def play_game():
    while True:
        min= 1
        max= 5
        target= random.randint(min,max)
        print("-----猜數字-----\n")
        print(f"答案是{target}")
        while True:
            keyin= int(input(f"請輸入{min}~{max}區間任一數字"))
            if min <= keyin <= max:
                if target == keyin:
                    print (f"答對了 答案是{keyin}")
                break
            else:
                if keyin >= target:
                    max = keyin -1
                    print(f"你輸入{keyin}。再小一點，請輸入{min}~{max}之間的數字")
                else:
                    if keyin <= target:
                        min = keyin +1
                        print(f"你輸入{keyin}。再大一點，請輸入{min}~{max}之間的數字")
            
                print("你猜的數字不在範圍內")
                continue
    
def main():
    while True:
        play_game()    
    play_again= input("再玩一次? [y/n]]")
    if play_again == 'n':   
        break

print("可以收書包回家")

main()

