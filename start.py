def startGame():
    import time, os
    valid = False
    while not valid:
        print("WELCOME TO SPACE INVADERS")
        time.sleep(2)
        print("I RECOMMEND YOU INCREASE THE HEIGHT OF THIS TERMINAL TO THE FULL HEIGHT OF YOUR SCREEN")
        time.sleep(2)
        print("INCREASING THE WIDTH OF THIS TERMINAL WILL MAKE THE GAME EASIER BUT COME ON YOU'RE BETTER THAN THAT")
        time.sleep(2)
        print("DECREASING THE WIDTH OF THIS TERMINAL WILL PROBABLY MAKE THE WHOLE THING S*** ITSELF SO DON'T")
        time.sleep(2)
        print("ALTHOUGH THAT DOES ASSUME SAME SETTINGS AS ME (DEFAULT) SO YOU MIGHT WANNA MESS ABOUT WITH IT")
        time.sleep(2)
        print("HINT, THE ABOVE LINE SHOULD GO ABOUT 3/4 - 4/5 ACROSS THE SCREEN")
        time.sleep(2)
        print("ENJOY")
        time.sleep(2)
        try:
            
            userStart = str(input("WHEN YOUR READY TO START, ENTER 'START' : "))
            if userStart.upper() == "START":
                valid = True
                import login
                username, highscore = login.login()
                import game
                game.play(username, highscore) 
            else:
                print(f"I GAVE YOU ONE INSTRUCTION, ENTER 'START' NOT '{userStart}' ")
                time.sleep(2)
                os.system("cls")
        except SystemExit as SE:
            pass
        except:
            valid = False
            print("WELL SOMETHING JUST BROKE, TRY AGAIN AND IF THIS CONTINUES SPAM ME WITH ANGRY MESSAGES")
            print("THE GAME WILL NOW START AGAIN")
            time.sleep(4)
            os.system("cls")
