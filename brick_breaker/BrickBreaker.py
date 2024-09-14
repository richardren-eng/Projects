#Richard Ren
#November 2022

import pygame as pg
pg.init() #Initialize all of pygame's modules.
import sys
import random 

game_font=pg.font.SysFont(None,50) #The font that will be used throughout the game.

difficulty=input("Would you like to play Easy, Normal, or Hard? Enter E, N, or H: ").upper()  #Ask the user what difficulty the user wants to play as.
while difficulty!='E' and difficulty!='N' and difficulty!='H':
        difficulty=input("Would you like to play Easy, Normal, or Hard? Enter E, N, or H: ").upper()  #Ask the user what difficulty the user wants to play as.

class colors:

    black=(0,0,0)
    white=(255,255,255)
    grey=(160,160,160)

    blue=(0,0,255)
    red=(215,35,35)
    green=(35,130,15)

    yellow=(202,246,56)
  
    
def MakeScreen(screenWidth, screenHeight):    
    
    #Set the game screen's dimensions.
    screen=pg.display.set_mode([int(screenWidth),int(screenHeight)])
    screen.fill(colors.grey)
    #Name the screen "Brick Destroyer"    
    
    pg.display.set_caption('Brick Breaker')
    #print("The screen's type is: "+str(type(screen)))
    return screen


#=============================ADJUST THESE PARAMETERS TO DETERMINE THE BEST SCREEN SIZE FOR THE GAME.=================================================================
screenWidth=880
screenHeight=600

screen=MakeScreen(screenWidth,screenHeight)


class Paddle(pg.sprite.Sprite): #pg.sprite.Sprite is a class for game sprites.
    """
    This is the paddle that the player controls with arrow keys.
    The paddle is a child of a pygame sprite class. 
    """
    def __init__(self):
        pg.sprite.Sprite.__init__(self) #Initialize the Paddle into a sprite.
    
        #Create the paddle as a rectangle. 
        if difficulty=='E':
            self.paddle_width=90
        elif difficulty=='N':
            self.paddle_width=80
        elif difficulty=='H':
            self.paddle_width=55
        
        self.paddle_height=15

        #Pygame.Surface defaulty creates a rectangle. 
        self.image=pg.Surface((self.paddle_width,self.paddle_height)) 
        self.image.fill(colors.black)
        
        #The rectangular area of the Paddle is simply the rectangular area of the paddle's image.
        self.rect=self.image.get_rect()
        
        #The paddle will start out in the middle-bottom of the screen.
        self.rect.centerx=screenWidth/2
        self.rect.centery=screenHeight-30

        #The paddle starts out with no speed i.e. no change in x-position. At the start, there are also no keys pressed.
        self.vx=0
        self.dx=5 #The number of pixels the paddle moves per key press.
        
    #Moves the paddle according to the user's key inputs.
    def update(self):
        keyPressed=pg.key.get_pressed()
        if keyPressed[pg.K_LEFT]:
            self.vx=-self.dx

        elif keyPressed[pg.K_RIGHT]:
            self.vx=self.dx
        
        self.rect.x+=self.vx
        
        #If the paddle tries to go off screen on the right side, set its x coordinate to the rightside of the screen so it can't move out.
        if self.rect.x+self.paddle_width>=screenWidth: #rect.x is the left side of the paddle so the rightside x position is rect.x + paddle_width.
            self.rect.x=screenWidth-self.paddle_width   

        #If the paddle tries to go out of bounds on the left, set its x position to 0 so it can't move out anymore.
        if self.rect.x<=0:
            self.rect.x=0


class Bricks():
    def __init__(self):
        self.rows=6 #The number of rows of bricks.
        self.cols=8 #The number of columns of bricks.
        self.width=screenWidth//self.cols #The width of each brick.
        self.height=25

    def create_bricks(self):
        self.bricks=[] #Contains every single brick that is going to be on the map.
        individual_brick=[] #Individual brick.
        
        #Iterate through the rows and columns to create the wall of bricks.
        for row in range(self.rows):
            brick_row=[] #clear the brick row list and get ready to create the next row.

            for col in range(self.cols):
                #generate coordinates for each brick.
                brick_x=col*self.width
                brick_y=row*self.height
                rect=pg.Rect(brick_x,brick_y,self.width,self.height)

                #Assign the number of lives each brick has.
                if row<2:
                    brick_strength=3
                elif row<4:
                    brick_strength=2
                elif row<6:
                    brick_strength=1

                #Create a list that contains the rect and strength data of the bricks.
                individual_brick=[rect,brick_strength]

                #Append the individual_brick to the total brick list.
                brick_row.append(individual_brick)
                
            #After the col loop is finished, a single row will have been created. Append that row to the total self.brick[] list and then repeat the col loop with a different row to create another row. 
            self.bricks.append(brick_row)    

    def spawn_bricks(self):
        for row in self.bricks:
            for brick in row:
                #Assign a color based on the strength of the brick. Strongest brick is red, medium brick is yellow, weakest brick is green.
                if brick[1] ==3: #If the strength which is the second index of the individual brick list is 3, the brick is red.
                    brick_color=colors.red
                elif brick[1] == 2:
                    brick_color=colors.yellow
                elif brick[1] == 1:
                    brick_color=colors.green
                
                #Draw the bricks.
                pg.draw.rect(screen,brick_color,brick[0]) #brick[0] is the coordinates of the rectangle of the brick.

                #Draw a border around each brick to separate them.
                pg.draw.rect(screen,colors.grey,brick[0],1)


class Ball(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self) #Initialize the ball into a sprite.
        
        self.width=15 #width of ball.
        self.image=pg.Surface((self.width,self.width)) #The ball's outline.
        self.image.fill(colors.blue) #Color the ball.
        

        self.rect=self.image.get_rect() #Get the rectangular outline of the ball.
        
        #The ball starts sitting on top of the paddle.
        self.rect.centerx=screenWidth/2
        self.rect.bottom=paddle.rect.top

        #The ball will have a random direction of initial velocity to keep things interesting. 
        self.vx=random.choice([-3,3])
        self.vy=-3

    def update(self):
        #Update the position of the ball.
        self.rect.x += self.vx
        self.rect.y += self.vy

        #If the ball is trying to go off of the screen at the top, assuming inelastic collision, reverse its vertical velocity component.
        if self.rect.top<=0:
            self.vy*=-1
        
        #If the ball is trying to go off screen at the left or right, assuming inelastic collision, revers the horizontal velocity components.
        if self.rect.left<=0:
            self.vx*=-1
        
        if self.rect.right>=screenWidth:
            self.vx*=-1


        collision_thresh=8 #If the absolute distance in x or y direction between the ball and a brick/paddle is less than the collision threshold of however many pixels, then it counts as a collision. This is used because sometimes, the ball will imbed itself into the paddle or a brick and end up spazzing out or breaking a brick multiple times in a single hit.

        #Collision with Paddle.
        collisionBP=pg.sprite.collide_rect(ball,paddle)
    
        #If the ball collides with the paddle, assuming inelastic collision, reverse both of the velocity components.
        if collisionBP:
            if abs(self.rect.bottom-paddle.rect.top)<collision_thresh: #If the collision threshold is satisifed, reverse the y component and velocity and give a random x component of velocity direction.
                self.vx*=random.choice([-1,1]) #Keep it interesting by giving the ball a random x-direction post collision.
                self.vy*=-1
        
        #In the slim chance that the ball loses all of its horizontal velocity, restore it so that the ball isn't just bouncing up and down.
        if self.vx==0:
            self.vx=random.choice([-3,3])

        #In the slim chance that the ball loses all of its vertical velocity, resotre it so that the ball isn't just bouncing left and right.
        if self.vy==0:
            self.vy=random.choice([-3,3])

    
        #Collision of ball with bricks.
        
        wall_destroyed=True #Start off assuming that the wall is destroyed. The code below checks for if there are any bricks that are still alive, and if there are, the wall_destroyed boolean will be changed to False. If the wall_destroted boolean is still True after the below code has checked to see if any bricks remain, then the user wins.        
        row_count=0
        for row in wall.bricks:
            item_count=0
            for item in row:
                #Check for collision between ball and brick.
                if self.rect.colliderect(item[0]):
                    #If the ball hits the top or bottom of a brick, reverse the y component of velocity.
                    if abs(self.rect.bottom-item[0].top)<collision_thresh or abs(self.rect.top-item[0].bottom)<collision_thresh:
                        self.vy*=-1
                            
                    #If the ball hits hits the left or right of a brick, reverse the x component of velocity.
                    if abs(self.rect.left-item[0].right)<collision_thresh or abs(self.rect.right-item[0].left)<collision_thresh:
                        self.vx*=-1

                    #Reduce the strength of the brick that got hit or eliminate the brick if it is out of health.
                    if wall.bricks[row_count][item_count][1]>1:
                        wall.bricks[row_count][item_count][1]-=1
                   
                    #Make the rectangle have 0 area if the brick is completely destroyed.
                    elif wall.bricks[row_count][item_count][1]==1:
                        wall.bricks[row_count][item_count][0] = (0,0,0,0) 
                        
                #Check if any bricks are still standing.
                if wall.bricks[row_count][item_count][0] != (0,0,0,0):
                    wall_destroyed=False
                    
                #Go to the next item in the row.
                item_count+=1
            #Go to the next row.
            row_count+=1
        #After checking every brick, check if the entire wall is destroyed.
        if wall_destroyed==True:
            lives.game_over='win'


class Lives():
    def __init__(self):
        self.lives=3
        self.game_over='restart' #Initiate the lives.game_over attribute so it can be called in the Ball() class.
    
    def update(self):
        #If the ball goes out of bounds at the bottom, take away a life and reset the positions of the ball and paddle.
        if ball.rect.top>screenHeight:
            self.lives-=1
            ball.__init__() #Reset the ball by reinitializing the ball class.
            paddle.__init__() #Reset the paddle.
        #Render the text.
        self.displayed_lives=game_font.render('Lives '+ str(self.lives),True,colors.black,colors.grey)

        if self.lives<=0:
            self.game_over='lose'
            
    def blit_lives(self): #Blit the text to the screen.
        #Get the rectangular text box surrounding the Lives display.
        lives_rect=self.displayed_lives.get_rect()
        
        #Center the text box to the middle of the screen.
        lives_rect.centerx=screenWidth/2
        lives_rect.centery=screenHeight/2+wall.height

        #Blit the text to the screen. If the game has been won, blit the number of lives display off of the gamescreen so it's not visible.
        if self.game_over!='win':        
            screen.blit(self.displayed_lives,lives_rect)
        else:
            screen.blit(self.displayed_lives,(screenWidth*2,screenHeight*2))

    def conclude_game(self):
        lose_text=game_font.render('YOU LOSE',True,colors.black,colors.grey)
        lose_rect=lose_text.get_rect()
        lose_rect.centerx=screenWidth/2
        lose_rect.centery=screenHeight/2+wall.height

        restart_text=game_font.render('Press Space to restart.',True,colors.black,colors.grey)
        restart_rect=restart_text.get_rect()
        restart_rect.centerx=screenWidth/2
        restart_rect.centery=lose_rect.centery+30
        
        win_text=game_font.render("YOU WIN",True,colors.black,colors.grey)
        win_rect=win_text.get_rect()
        win_rect.centerx=screenWidth/2
        win_rect.centery=screenHeight/2+wall.height


        #If the player loses, reset the ball to be stationary and display the game lost text.
        if self.game_over == 'lose':
            ball.__init__() #Reset the ball.
            ball.vx=0
            ball.vy=0
            screen.blit(lose_text,lose_rect)
            screen.blit(restart_text,restart_rect)
        
        #If the player wins, reset the ball to be stationary and display the game win text.
        if self.game_over == 'win':
            ball.__init__()
            ball.vx=0
            ball.vy=0
            screen.blit(win_text,win_rect)
            screen.blit(restart_text,restart_rect)


#Initiate the classes.
paddle=Paddle()
ball=Ball()
lives=Lives()
wall=Bricks()

#Create single sprite group for the paddle sprite.
paddle_sprite=pg.sprite.GroupSingle()
paddle_sprite.add(paddle)

#Create single sprite group for ball sprite.
ball_sprite=pg.sprite.GroupSingle()
ball_sprite.add(ball)


def main():
    
    wall.create_bricks() #Create the brick wall.
    
    #Initialize the game loop.
    #Define a clock.
    clock=pg.time.Clock()
    
    #Set the gamespeed depending on the difficulty.
    if difficulty=='E':
        fps=120
    elif difficulty=='N':
        fps=130
    elif difficulty=='H':
        fps=150
    
    
    running = True
    paddle.__init__()
    ball.__init__()
    lives.__init__()
    wall.__init__()
    
    while running:
        clock.tick(fps)
        #Get events that occur in the game. If a quit game event is triggered, quit the game.
        for event in pg.event.get():
        #Quit running and close everything if a quit condition event is detected.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        #Erase the previous frame by filling the screen grey.
        screen.fill(colors.grey)

        #Spawn the bricks.
        wall.spawn_bricks()

        #Update the positions of the sprites.
        paddle_sprite.update()
        paddle.vx=0 #Set the paddle speed back to 0 after the user input so that the paddle doesn't keep moving.
        ball_sprite.update()
        lives.update()

        #Draw the lives.
        lives.blit_lives()

        #See if the game has been won/lost.
        lives.conclude_game()

        #Draw Sprites.
        paddle_sprite.draw(screen)
        ball_sprite.draw(screen)

        #Show the next "stop motion" picture that was drawn.
        pg.display.flip()

        #If the user presses space when he/she has lost or won, restart the game.
        if lives.game_over=='lose' or lives.game_over=='win':
            for event in pg.event.get():
                if event.type==pg.KEYUP:
                    if event.key==pg.K_SPACE:
                        lives.game_over=''
                        main()
           

#This loop ensures that the game won't start until the user presses left or right for the first time.
while True:
    #Reset positions of paddle, ball, lives, and brick wall and set the ball to not move.
    paddle.__init__()
    ball.__init__()
    lives.__init__()
    wall.__init__()
    ball.vx=0
    ball.vy=0

    #Draw the sprites to the screen.
    paddle_sprite.draw(screen)
    ball_sprite.draw(screen)
    wall.create_bricks() #Create the brick wall.
    wall.spawn_bricks()

    #Display the instructions on screen.
    #Render the text.
    start_text=game_font.render("Use the Left and Right Arrow Keys to move.",True,colors.black,colors.grey)
    
    #Get the center coordinates of the instructions message.
    start_rect=start_text.get_rect()
    start_rect.centerx=screenWidth/2
    start_rect.centery=screenHeight/2+wall.height
    
    #Blit the instructions to the screen.
    screen.blit(start_text,start_rect)
    
    #Display all the sprites and instructions.
    pg.display.flip()
    
    #Don't start the game until the user moves left or right.
    for event in pg.event.get():
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_RIGHT or event.key==pg.K_LEFT:
                main()    
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


print('Quitting game due to error')
pg.quit()
sys.exit()









