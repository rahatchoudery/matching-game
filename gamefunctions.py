import pygame
import os

class Game(object):

    def __init__(self, window_width, window_height, window_title):
        pygame.init()
        pygame.font.init()

        self.window_title = window_title
        self.window_width = window_width
        self.window_height = window_height

        # How the text prompt looks
        self.prompt_token = chr(187) + "   "

        # Choice variables
        self.current_choice = 0
        self.choice = []
        self.choice_spacing = 20

        # Font setup
        self.font_name = pygame.font.get_default_font()
        self.font_size = 22
        self.font_color = (0,0,0) # black is default
        self.unselected_font_color = (120,120,120) # grey
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

        # These make a new window appear on the screen
        pygame.display.set_caption(self.window_title)
        pygame.display.set_mode((self.window_width, self.window_height))
        self.screen = pygame.display.get_surface()
        self.wait_mode = None

        # This is the list of things to draw to the screen.
        # It get cleared at the start of each newFrame()
        self.stuff_to_draw = []

        # These set up timing for updating the screen when waiting on input
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.keys = pygame.key.get_pressed()

    def setFont(self, font_name, font_size, font_color):
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.font = pygame.font.Font(self.font_name, self.font_size)

    def getSystemFonts(self):
        return pygame.font.get_fonts()

    def quit(self):
        # Close the game window
        pygame.quit()
        

    def mainLoop(self):
        while self.wait_mode is not None:
            self.eventLoop()
            self.render()
            self.clock.tick(self.fps)

    def eventLoop(self):
        
        for event in pygame.event.get():
            
            print('Top of event loop. wait=', self.wait_mode)
            
            # handle a hard exit first
            if event.type == pygame.QUIT:
                print('User has chosen to exit the game NOW!')
                self.wait_mode = None

            # Otherwise, if we're waiting for any signal to stop
            if self.wait_mode == 'anything':

                if (event.type == pygame.KEYDOWN or
                    event.type == pygame.MOUSEBUTTONDOWN):
                    self.wait_mode = None

            # Otherwise, is we're waiting for a mouse click
            elif self.wait_mode == 'click':

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_coords = event.pos
                    self.wait_mode = None

            # Otherwise, if we're waiting to typed text
            elif self.wait_mode == 'text_entry':

                # only consider key presses
                if event.type != pygame.KEYDOWN:
                    continue

                if pygame.K_SPACE <= event.key <= pygame.K_z:
                    self.text_entered = self.text_entered + event.unicode
                    label = self.font.render(self.prompt_token + self.text_entered, True, self.font_color)
                    x_coord, y_coord, _ = self.stuff_to_draw[-1]
                    self.stuff_to_draw[-1] = (x_coord, y_coord, label)
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text_entered) > 0:
                        self.text_entered = self.text_entered[0:-2]
                    label = self.font.render(self.prompt_token + self.text_entered, True, self.font_color)
                    x_coord, y_coord, _ = self.stuff_to_draw[-1]
                    self.stuff_to_draw[-1] = (x_coord, y_coord, label)
                elif event.key == pygame.K_RETURN:
                    self.wait_mode = None
                else:
                    print('other key pressed:', event.key)

            # Otherwise, if we're waiting for multiple choices
            elif self.wait_mode == 'choice':

                # Are we done waiting for a choice?
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN:
                        self.wait_mode = None
                    elif event.key == pygame.K_DOWN:
                        self.current_choice = (self.current_choice + 1) % len(self.choices)
                    elif event.key == pygame.K_UP:
                        self.current_choice = (self.current_choice - 1) % len(self.choices)
                    else:
                        continue # Not an arrow key, so move on

                    # Redraw
                    N = len(self.stuff_to_draw)
                    M = len(self.choices)
                    for k, c in enumerate(self.choices):
                        if k == self.current_choice:
                            color = self.font_color
                        else:
                            color = self.unselected_font_color
                        print('k=', k, 'color=', color)
                        x_coord, y_coord, _ = self.stuff_to_draw[N-M+k]
                        label = self.font.render(c, True, color)
                        self.stuff_to_draw[N-M+k] = (x_coord, y_coord, label)
                    print(self.stuff_to_draw)

            
            # This shouldn't happen
            #else:
            #    raise ValueError("Invalid wait mode={}. Something is broken in the engine.".format(self.wait_mode))

    def render(self):
        self.screen.fill((255,255,255))
        for x_coord, y_coord, blip in self.stuff_to_draw:
            self.screen.blit(blip, (x_coord, y_coord))
        pygame.display.flip()

    def newFrame(self):
        self.wait_mode = None
        self.stuff_to_draw = []
        self.render()

    def addImage(self, image_name, x_coord, y_coord):
        if os.path.isfile(image_name):
            image = pygame.image.load(image_name).convert()
            self.stuff_to_draw.append((x_coord, y_coord, image))
            self.render()
        else:
            raise Warning("addImage failed: the file {} doesn't seem to exist!".format(image_name))


    def addText(self, text, x_coord, y_coord):
        """
        Draw the specified text to the screen, at pixel location x,y.
        Use the specified RGB color (each number between 0 and 255).
        """
        label = self.font.render(text, True, self.font_color)
        self.stuff_to_draw.append((x_coord, y_coord, label))
        self.render()

    def waitForChoice(self, choices, x_coord, y_coord):
        if len(choices) == 0:
            raise ValueError("waitForChoice called with no choices!")
        self.wait_mode = 'choice'
        self.current_choice = 0
        self.choices = choices
        for k, c in enumerate(self.choices):
            if k == self.current_choice:
                color = self.font_color
            else:
                color = self.unselected_font_color

            label = self.font.render(c, True, color)
            self.stuff_to_draw.append((x_coord, y_coord + k * self.choice_spacing, label))
        self.mainLoop()
        return self.current_choice

    def waitForText(self, x_coord, y_coord):
        self.wait_mode = 'text_entry'
        self.text_entered = ''
        label = self.font.render(self.prompt_token, True, self.font_color)
        self.stuff_to_draw.append((x_coord, y_coord, label))
        self.mainLoop()
        return self.text_entered

    def waitForClick(self):
        self.wait_mode = 'click'
        self.mainLoop()
        return self.click_coords

    def waitForAnything(self):
        self.wait_mode = 'anything'
        self.mainLoop()
