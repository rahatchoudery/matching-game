import gamefunctions
from random import shuffle
from time import time

game = gamefunctions.Game(750, 600, "Christmas Matching Game")

#puts images of cards on screen
def cards():
    game.newFrame()
    game.addImage("background.jpg",0, 0) #found at https://pixabay.com/en/christmas-background-2988225/ 
    game.addImage("card_a.png",150, 75)
    game.addImage("card_b.png",400, 75)
    game.addImage("card_c.png",150, 250)
    game.addImage("card_d.png",400, 250)

#how to play instructions          
def how_to_play():
    game.newFrame()
    game.addImage("background.jpg",0, 0)
    game.setFont('Times New Roman.ttf', 24, (0,128,0))
    game.addText("You will be given 4 cards to choose from.", 20, 100)
    game.addText("Pick your first card.", 20, 150)
    game.addText("Then, pick your second card.", 20, 200)
    game.addText("You will be shown whether or not your choices are a match.", 20, 250)
    game.addText("You can then choose whether or not you want to play again.", 20, 300)
    game.addText("Get 5 matches and you win the game!", 20, 350)
    game.addText("Try to get 5 matches in under 30 seconds!", 20, 400)
    game.setFont('Times New Roman.ttf', 24, (200,0,0))
    game.addText("Click anywhere on this screen to return to the main menu.", 20, 450)


#make title screen
def main_screen():
    game.newFrame()
    game.addImage("title_screen.jpg",0, 0) #found at https://pixabay.com/en/christmas-christmas-tree-decorate-1869902/
    game.setFont('Times New Roman.ttf', 24, (0,128,0))
    game.unselected_font_color = (255,255,255)
    choice = game.waitForChoice(["Start Game", "How To Play"], 500, 200)
#if player chooses "how to play", go to how to play screen
#when the user clicks on the screen, go to main screen
#if user chooses "start game", go to matching game
    if choice == (1):
        how_to_play()
        game.waitForClick()
        main_screen()
    else:
        matching_game()
        
def matching_game():
    i = True
        #Keep Score
    count = 0
    #begins timer
    start = time()
    #boolean that later determines whether user finished in a fast or slow time
    fast = False
    best_time = 30.00
    while count >= 0 and count <= 5:
        while i == True:
            cards()
            #assign images and shuffle them each time
            images = ["pic_1.png", "pic_2.png", "pic_1.png", "pic_2.png"]
            shuffle(images)
            #whenever players chooses a card, give the other three cards as options for second pick         
            game.setFont('Times New Roman.ttf', 24, (0,128,0))
            game.addText("Pick your first card", 50, 425)
            game.setFont('Times New Roman.ttf', 24, (128,0,0))
            game.unselected_font_color = (0,0,0)
            options_1 = game.waitForChoice(["Card A", "Card B", "Card C", "Card D" ], 50, 450)
                    
            
            #if user picks Card A
            if options_1 == (0):
                user_pick_a = images[0]
                game.setFont('Times New Roman.ttf', 24, (0,128,0))
                game.addText("Pick your second card", 500, 425)
                game.setFont('Times New Roman.ttf', 24, (128,0,0))
                game.unselected_font_color = (0,0,0)
                options_2 = game.waitForChoice(["Card B", "Card C", "Card D" ], 500, 450)
             
                if options_2 == (0):
                    user_pick_b = images[1]
                    
                elif options_2 == (1):
                    user_pick_b = images[2]
                    
                else:
                    user_pick_b = images[3]
                    
            #if user picks Card B
            elif options_1 == (1):
                user_pick_a = images[1]
                game.setFont('Times New Roman.ttf', 24, (0,128,0))
                game.addText("Pick your second card", 500, 425)
                game.setFont('Times New Roman.ttf', 24, (128,0,0))
                game.unselected_font_color = (0,0,0)
                options_2 = game.waitForChoice(["Card A", "Card C", "Card D" ], 500, 450)
                
                if options_2 == (0):
                    user_pick_b = images[0]
                    
                elif options_2 == (1):
                    user_pick_b = images[2]
                    
                else:
                    user_pick_b = images[3]
            
            #if user picks Card C
            elif options_1 == (2):
                user_pick_a = images[2]
                game.setFont('Times New Roman.ttf', 24, (0,128,0))
                game.addText("Pick your second card", 500, 425)
                game.setFont('Times New Roman.ttf', 24, (128,0,0))
                game.unselected_font_color = (0,0,0)
                options_2 = game.waitForChoice(["Card A", "Card B", "Card D" ], 500, 450)
                
                if options_2 == (0):
                    user_pick_b = images[0]
                    
                elif options_2 == (1):
                    user_pick_b = images[1]
                    
                else:
                    user_pick_b = images[3]
               
            #if user picks Card D
            else:
                user_pick_a = images[3]
                game.setFont('Times New Roman.ttf', 24, (0,128,0))
                game.addText("Pick your second card", 500, 425)
                game.setFont('Times New Roman.ttf', 24, (128,0,0))
                game.unselected_font_color = (0,0,0)
                options_2 = game.waitForChoice(["Card A", "Card B", "Card C" ], 500, 450)
                
                if options_2 == (0):
                    user_pick_b = images[0]
                    
                elif options_2 == (1):
                    user_pick_b = images[1]
                    
                else:
                    user_pick_b = images[2]
                    
          #Results Page
            game.newFrame()
            game.addImage("background4.jpg",0, 0) #found at http://www.publicdomainfiles.com/show_file.php?id=14003493619627
            if user_pick_a == user_pick_b:
                count += 1
                game.addImage(user_pick_a ,200, 200)
                game.addImage(user_pick_b ,400, 200)
                game.setFont('Times New Roman.ttf', 40, (0,128,0))
                game.addText("It's a match!", 275, 450)
                game.addText("Click anywhere to continue.", 160, 500)
                #if there is a match, add to score
                
            else:
                game.addImage(user_pick_a ,200, 200)
                game.addImage(user_pick_b ,400, 200)
                game.setFont('Times New Roman.ttf', 40, (255,0,0))
                game.addText("Not a match!", 275, 450)
                game.addText("Click anywhere to continue.", 160, 500)
            game.waitForClick() 
     
           # Exit Page
            game.newFrame()
            game.setFont('Times New Roman.ttf', 24, (0,128,0))
            game.unselected_font_color = (128,0,0)
            game.addImage("background5.jpg",0, 0) #found on https://pixabay.com/en/background-backdrop-christmas-2997306/
            game.addText("Total Score: " + str(count), 400, 150)
            #once user reaches 5 matches
            if count == 5:
                end = time()
                total_time = round((end - start), 2)
                if total_time <= best_time:
                    fast = True
                if fast:
                    game.addText("That was fast! Did you cheat?", 400, 175)
                else:
                    game.addText("A little on the slow side!", 400, 175)
                game.addText("You won in " + str(total_time) + " seconds", 400, 200)
                game.addText("Would you like to play again?", 400, 250)
                yes_no = game.waitForChoice(["Yes", "No"], 400, 300)
            #User ends game, exit while loop
                while yes_no != (0):
                    i = False
                #if user chooses to play again, score resets, timer resets, and boolean for 
                #finishing speed resets to false
                count = 0
                start = time()
                fast = False
                    
            else:
                game.addText("Would you like to play again?", 400, 250)
                yes_no = game.waitForChoice(["Yes", "No"], 400, 300)
            #User ends game, exit while loop
                if yes_no == (1):
                    i = False
            
main_screen()  
       
game.quit()