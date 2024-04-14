from pygame import *
from random import randint

fps = 60
game_finished, game_run = False, True
clock = time.Clock()


window_width, window_height = 1365, 700

kills, lost,  = 0, 0,

in_menu = True

window = display.set_mode((window_width, window_height))
display.set_caption("shooter by Иля")


font.init()

score_font = font.SysFont("Arial", 32, True)
main_font = font.SysFont("Arial", 72, True)


mixer.init()
music=mixer.Sound("(Дляигрывшутеры31)KhaosHammer-Battlefield4MainThemeSong_(muzmo.su).mp3")
music.play()
fire_sound = mixer.Sound("z_uk-vystrel-s-pistoleta.mp3")
miss_sound = mixer.Sound("damage1.mp3")
kill_sound = mixer.Sound("death2.mp3")
lose_sound = mixer.Sound("game-lost.mp3")
win_sound = mixer.Sound("game-won.mp3")

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


class Pulya(GameSprite):
    def update(self):
        global kills
        
        self.rect.y -= self.speed

        enemys_collided_list = sprite.spritecollide(self,enemys_group, False)

        if len(enemys_collided_list) > 0:
            enemy = enemys_collided_list[0]

            if enemy.health > 1:
                enemy.health -= 1
            else:
                enemy.kill()
                kills +=1

            
            kill_sound.play()
            self.kill()

        if self.rect.y <= 0:
            self.kill()



bg = GameSprite(img = "bg.jpg", pos=(0, 0), size=(window_width, window_height), speed = 0)
player = Player(img = "igrok.png", pos=(5, window_height - 64), size=(96, 64), speed = 5)

enemys_group = sprite.Group()

gryppa_pylb = sprite.Group()


enemys_spawn_delay = fps
enemys_spawn_timer = enemys_spawn_delay

while game_run:
    for ev in event.get():
        if ev.type == QUIT:
            game_run = False
        if ev.type == KEYDOWN:
            if ev.key == K_ESCAPE:
                in_menu = not in_menu
            if ev.key == K_z:
                pass
    
    if not in_menu: 
        bg.reset()

        player.reset()
        enemys_group.draw(window)
        gryppa_pylb.draw(window)
    
        kills_text = score_font.render("Ybito: " + str(kills), True, (255, 255,255))
        lost_text = score_font.render("Propyscheno: "+ str(lost), True, (255,255,255))

        window.blit(kills_text, (5,5))
        window.blit(lost_text, (5,37))

        if kills >= 15:
            screen_text = main_font.render("Ti pobedil!!!", True, (0,255,0))
            window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
            fire_sound.stop()
            music.stop()
            win_sound.play()

            game_finished = True
        
        if lost >= 15:
            screen_text = main_font.render("Ti proigral lox!", True, (255,0,0))
            window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
            music.stop()
            fire_sound.stop()
            lose_sound.play()

            game_finished = True

        if not game_finished:
            r = randint(1, 3)
            if enemys_spawn_timer > 0:
                enemys_spawn_timer -= 1
            elif r == 1:
                new_enemy = Enemy(img="vrag.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 5), health = 3 )
                enemys_group.add(new_enemy)
                enemys_spawn_timer = enemys_spawn_delay
            elif r == 2:
                new_enemy = Enemy(img="vrag3.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 5), health = 2 )
                enemys_group.add(new_enemy)
                enemys_spawn_timer = enemys_spawn_delay
            elif r == 3:
                new_enemy = Enemy(img="vrag2.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 5), health = 1 )
                enemys_group.add(new_enemy)
                enemys_spawn_timer = enemys_spawn_delay
            player.update()
            enemys_group.update()
            gryppa_pylb.update()
    else:
        window.fill((200, 200, 200))
    display.update()
    clock.tick(fps)
