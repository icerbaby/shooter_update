from pygame import *
from random import randint

fps = 60
game_finished, game_run, game_paused, game_finished2 = False, True, False, False
clock = time.Clock()


window_width, window_height = 1115, 570

kills, lost,  = 0, 0,

in_menu = True

in_stopmenu = False

osoboye_menu = False

boss_killed = False

window = display.set_mode((window_width, window_height))
display.set_caption("Илья маладес")


font.init()

score_font = font.SysFont("Arial", 32, True)
main_font = font.SysFont("Arial", 72, True)


mixer.init()
music=mixer.Sound("Дляигрывшутеры31KhaosHammer_Battlefield4MainThemeSong_muzmo_su.mp3")
music.play()
fire_sound = mixer.Sound("z_uk-vystrel-s-pistoleta.mp3")
miss_sound = mixer.Sound("damage1.mp3")
kill_sound = mixer.Sound("death2.mp3")
lose_sound = mixer.Sound("game-lost.mp3")
win_sound = mixer.Sound("game-won.mp3")

class Menu:
    def __init__(self):
        window.fill((200,200,200))
        self.font = font.Font(None, 36)
        self.difficulty1_button = Rect(200, window_height /2, 180, 50)
        self.difficulty2_button = Rect(500, window_height /2, 190, 50)
        self.difficulty3_button = Rect(800, window_height /2, 180, 50)
        self.difficulty3_text = self.font.render("Сложная", True, (255, 255, 255))
        self.difficulty2_text = self.font.render("Средняя", True, (255, 255, 255))
        self.difficulty1_text = self.font.render("Легкая", True, (255, 255, 255))

        self.simple_text = self.font.render("Выбери сложность для начала игры", True, (255, 255, 255))
    
    def draw_buttons(self):
        window.fill((0, 0, 0))  
        draw.rect(window, (200, 200, 200), self.difficulty1_button)  
        draw.rect(window, (200, 200, 200), self.difficulty2_button)
        draw.rect(window, (200, 200, 200), self.difficulty3_button)  
        window.blit(self.difficulty1_text, (self.difficulty1_button.x + 50, self.difficulty1_button.y + 10))  
        window.blit(self.difficulty2_text, (self.difficulty2_button.x + 55, self.difficulty2_button.y + 10))
        window.blit(self.difficulty3_text, (self.difficulty3_button.x + 55, self.difficulty3_button.y + 10))
        window.blit(self.simple_text, (window_width - 750, 120))

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.difficulty1_button.collidepoint(mouse.get_pos()):  
                return "Легкая"  
            elif self.difficulty2_button.collidepoint(mouse.get_pos()):  
                return "Средняя"
            elif self.difficulty3_button.collidepoint(mouse.get_pos()):
                return "Сложная"    
        return None
    
    
    

class StopMenu:
    def __init__(self):
        window.fill((200,200,200))
        self.font = font.Font(None, 36)
        self.continue_button = Rect(200, window_height /2, 180, 50)
        self.exit_button = Rect(500, window_height /2, 190, 50)
        self.continue_text = self.font.render("Продолжить", True, (255, 255, 255))
        self.exit_text = self.font.render("Выход", True, (255, 255, 255))


    def draw_buttons2(self):
        window.fill(0,0,0)
        draw.rect(window, (255, 255, 255), self.continue_button)  
        draw.rect(window, (255, 255, 255), self.exit_button)
        window.blit(self.exit_text, (self.continue_button.x + 50, self.continue_button.y + 10))  
        window.blit(self.continue_text, (self.exit_button.x + 55, self.exit_button.y + 10))

    def actions(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(mouse.get_pos()):  
                return "Продолжить"  
            elif self.exit_button.collidepoint(mouse.get_pos()):  
                return "Выход"   
        return None

        



class GameSprite(sprite.Sprite):
    def __init__(self, img, pos, size, speed,):
        super().__init__()

        
        self.image = transform.smoothscale(
            image.load(img),
            size
        )

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        self.speed = speed
        self.width, self.height = size

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    fire_delay = fps * 0.25
    fire_timer = fire_delay
    can_fire = True

    def update(self):

        if not self.can_fire:
            if self.fire_timer > 0:
                self.fire_timer -= 1
            else:
                self.fire_timer = self.fire_delay
                self.can_fire = True
            

        keys = key.get_pressed()
        if keys[K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[K_d]:
            if self.rect.x < window_width - self.width:
                self.rect.x += self.speed

        if keys[K_SPACE] and self.can_fire:
            fire_sound.play()
            self.fire()
            self.can_fire = False
    def fire(self):
        new_pylya = Pulya(img="pylya.png", pos=(self.rect.x, self.rect.y), size=(100, 100), speed=15)

        gryppa_pylb.add(new_pylya)
        

class Enemy(GameSprite):
    def __init__(self, img, pos, size, speed, health):
        super().__init__(img, pos, size, speed)
        self.health = health

        


    def update(self):
        global lost
        
        self.health_font = score_font.render(str(self.health), True, (255, 255,255))
        window.blit(self.health_font, self.rect.topright)
        self.rect.y += self.speed
        if self.rect.y >= window_height or sprite.collide_rect(self, player):
            lost += 1
            miss_sound.play()
            self.kill()

class Boss(GameSprite):
    def __init__(self, img, pos, size, speed, health):
        super().__init__(img, pos, size, speed)
        self.health = health

        


    def update(self):
        global lost
        
        self.health_font = score_font.render(str(self.health), True, (255, 255,255))
        window.blit(self.health_font, self.rect.topright)
        self.rect.y += self.speed
        if self.rect.y >= window_height or sprite.collide_rect(self, player):
            screen_text = main_font.render("Ты проиграл(", True, (255,0,0))
            window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
            music.stop()
            fire_sound.stop()
            lose_sound.play()
            self.kill()
            game_finished = True



class Pulya(GameSprite):
    def update(self):
        global kills
        global game_finished2
        global boss_killed
        
        self.rect.y -= self.speed

        enemys_collided_list = sprite.spritecollide(self,enemys_group, False)

        bosses_collided_list = sprite.spritecollide(self,bosses_group, False)

        if len(enemys_collided_list) > 0:
            enemy = enemys_collided_list[0]

            if enemy.health > 1:
                enemy.health -= 1
                self.kill()
            else:
                enemy.kill()
                self.kill()
                kills +=1

        
        
        if len(bosses_collided_list) > 0:
            boss = bosses_collided_list[0]

            if boss.health > 1:
                boss.health -=1
                self.kill
            else:
                boss.kill()
                self.kill()
                boss_killed = True
                
                game_finished2 = True

            
            kill_sound.play()
            self.kill()

        if self.rect.y <= 0:
            self.kill()



bg = GameSprite(img = "bg.jpg", pos=(0, 0), size=(window_width, window_height), speed = 0)
player = Player(img = "igrok.png", pos=(5, window_height - 64), size=(96, 64), speed = 5)
menu = Menu()
stopmenu= StopMenu()


enemys_group = sprite.Group()

bosses_group = sprite.Group()

gryppa_pylb = sprite.Group()


bosses_spawn_delay = fps 
bosses_spawn_timer = fps * 10000

enemys_spawn_delay = fps
enemys_spawn_timer = enemys_spawn_delay

while in_menu:
    music.stop()
    for ev in event.get():
        if ev.type == QUIT:
            in_menu = False
            game_run = False
    menu.draw_buttons()
    display.update()



    for ev in event.get():
        action = menu.handle_event(ev)
        if action == "Сложная" and in_menu:
            in_menu = False
        elif action == "Средняя" and in_menu:
            in_menu = False
        elif action == "Легкая" and in_menu:
            in_menu = False

while in_stopmenu:
    music.stop()
    for ev in event.get():
        if ev.type == QUIT:
            in_stopmenu = False
            game_run = False
    
    stopmenu.draw_buttons2()
    display.update()



while game_run:
    for ev in event.get():
        if ev.type == QUIT:
            game_run = False
        keys = key.get_pressed()
        if ev.type == KEYDOWN:
            if ev.key == K_ESCAPE:
                
                in_menu = not in_menu

        
    if not in_menu and action == "Легкая":
        bg.reset()
        player.reset()
        bosses_group.draw(window)
        gryppa_pylb.draw(window)
    
        kills_text = score_font.render("Убито: " + str(kills), True, (255, 255,255))
        lost_text = score_font.render("Пропущено: "+ str(lost), True, (255,255,255))

        window.blit(kills_text, (5,5))
        window.blit(lost_text, (5,37))

        if kills >= 10:
            game_paused = True
            bosses_spawn_delay -=1
            if bosses_spawn_delay == 0:
                bosses_spawn_delay = bosses_spawn_timer
            
                easy_boss = Boss(img = "easy_boss.png", pos=(window_width /2, 0), size = (192, 128), speed = 0.5, health = 10)
                bosses_group.add(easy_boss)
            if boss_killed == True:
                screen_text = main_font.render("Ты выиграл!", True, (255,255,0))
                window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
                music.stop()
                fire_sound.stop()
                win_sound.play()
                
                   
                    
            
           


            
        
        if lost >= 15:
            screen_text = main_font.render("Ты проиграл(", True, (255,0,0))
            window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
            music.stop()
            fire_sound.stop()
            lose_sound.play()
            game_finished2 = True
            game_finished = True
        if not game_finished2:
            if not game_finished and not game_paused:
                r = randint(1,3)
                if enemys_spawn_timer > 0:
                    enemys_spawn_timer -= 1
                else:
                    if r == 1:
                        new_enemy = Enemy(img="vrag.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 5), health = 3 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                    if r == 2:
                        new_enemy = Enemy(img="vrag2.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 5), health = 2 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                    if r== 3:
                        new_enemy = Enemy(img="vrag3.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 1 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                enemys_group.draw(window)
                enemys_group.update()
            bosses_group.update()
            player.update()
            gryppa_pylb.update()   
            
                
    elif not in_menu and action == "Средняя":
        bg.reset()
        player.reset()
        bosses_group.draw(window)
        gryppa_pylb.draw(window)
    
        kills_text = score_font.render("Убито: " + str(kills), True, (255, 255,255))
        lost_text = score_font.render("Пропущено: "+ str(lost), True, (255,255,255))

        window.blit(kills_text, (5,5))
        window.blit(lost_text, (5,37))

        if kills >= 15:
            game_paused = True
            bosses_spawn_delay -=1
            if bosses_spawn_delay == 0:
                bosses_spawn_delay = bosses_spawn_timer
            
                medium_boss = Boss(img = "medium_boss.png", pos=(window_width /2, 0), size = (192, 128), speed = 0.5, health = 15)
                bosses_group.add(medium_boss)
            if boss_killed == True:
                screen_text = main_font.render("Ты выиграл!", True, (255,255,0))
                window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
                music.stop()
                fire_sound.stop()
                win_sound.play()
                
                   
                    
            
           


            
        
        if lost >= 10:
            screen_text = main_font.render("Ты проиграл(", True, (255,0,0))
            window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
            music.stop()
            fire_sound.stop()
            lose_sound.play()
            game_finished2 = True
            game_finished = True
        if not game_finished2:
            if not game_finished and not game_paused:
                r = randint(1,3)
                if enemys_spawn_timer > 0:
                    enemys_spawn_timer -= 1
                else:
                    if r == 1:
                        new_enemy = Enemy(img="vrag.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 3 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                    if r == 2:
                        new_enemy = Enemy(img="vrag2.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 2 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                    if r== 3:
                        new_enemy = Enemy(img="vrag3.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 1 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                enemys_group.draw(window)
                enemys_group.update()
            bosses_group.update()
            player.update()
            gryppa_pylb.update()
    elif not in_menu and action == "Сложная":
        bg.reset()
        player.reset()
        bosses_group.draw(window)
        gryppa_pylb.draw(window)
    
        kills_text = score_font.render("Убито: " + str(kills), True, (255, 255,255))
        lost_text = score_font.render("Пропущено: "+ str(lost), True, (255,255,255))

        window.blit(kills_text, (5,5))
        window.blit(lost_text, (5,37))

        if kills >= 20:
            game_paused = True
            bosses_spawn_delay -=1
            if bosses_spawn_delay == 0:
                bosses_spawn_delay = bosses_spawn_timer
            
                hard_boss = Boss(img = "hard_boss.png", pos=(window_width /2, 0), size = (192, 128), speed = 0.5, health = 20)
                bosses_group.add(hard_boss)
            if boss_killed == True:
                screen_text = main_font.render("Ты выиграл!", True, (255,255,0))
                window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
                music.stop()
                fire_sound.stop()
                win_sound.play()
                
                   
                    
            
           


            
        
        if lost >= 10:
            screen_text = main_font.render("Ты проиграл(", True, (255,0,0))
            window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
            music.stop()
            fire_sound.stop()
            lose_sound.play()
            game_finished2 = True
            game_finished = True
        if not game_finished2:
            if not game_finished and not game_paused:
                r = randint(1,3)
                if enemys_spawn_timer > 0:
                    enemys_spawn_timer -= 1
                else:
                    if r == 1:
                        new_enemy = Enemy(img="vrag.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 3 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                    if r == 2:
                        new_enemy = Enemy(img="vrag2.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 2 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                    if r== 3:
                        new_enemy = Enemy(img="vrag3.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 1 )
                        enemys_group.add(new_enemy)
                        enemys_spawn_timer = enemys_spawn_delay
                enemys_group.draw(window)
                enemys_group.update()
            bosses_group.update()
            player.update()
            gryppa_pylb.update()
    else:
        music.stop()
        fire_sound.stop()
        menu.draw_buttons()
            
    display.update()
    clock.tick(fps)
