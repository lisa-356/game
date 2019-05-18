from livewires import games, color
import random

games.init(screen_width=765, screen_height=430, fps=50)

'''Разрабатываем Посейдона'''


class Person(games.Sprite):
    image = games.load_image('image/person.png')

    def __init__(self):
        super(Person, self).__init__(image=Person.image, x=games.screen.width-60,y=games.screen.height/2)

        self.score = games.Text(value=3, size=50, right=games.screen.width/2, top=5, color=color.black)
        games.screen.add(self.score)

    def update(self):

        if games.keyboard.is_pressed(games.K_UP):
            self.y -= 1
        if games.keyboard.is_pressed(games.K_DOWN):
            self.y += 1
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += 1
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= 1
        if self.bottom > games.screen.height:
            self.bottom = games.screen.height
        if self.top < -10:
            self.top = -10
        self.check_catch()

    def check_catch(self):
        for shark in self.overlapping_sprites:
            shark.handle_caught()
            self.score.value -= 1
            if self.score.value == 0:
                self.end_game()
                self.destroy()
            self.check_catch()

    def end_game(self):
        end_msg = games.Message(value='You are loser',
                                size=90,
                                color=color.red,
                                x=games.screen.width / 2,
                                y=games.screen.height/2,
                                lifetime=5 * games.screen.fps,
                                after_death=games.screen.quit
                                )
        games.screen.add(end_msg)


class Magic(games.Sprite):

    image = games.load_image('image/shark.png')

    def __init__(self,  x=-20, speed=3, odds_change=100):
        super(Magic, self).__init__(image=Magic.image, x=x, y=games.screen.height/2, dy=speed)
        self.odds_change = odds_change
        self.time_til_drop = 0

    def update(self):
        if self.bottom > games.screen.height or self.top < 0:
            self.dy = -self.dy
        elif random.randrange(self.odds_change) == 0:
            self.dy = - self.dy
        self.check_drop()

    def check_drop(self):
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_shark = Shark(y=self.y)
            games.screen.add(new_shark)

            self.time_til_drop = random.randint(100, 600)


class Shark(games.Sprite):

    image = games.load_image('image/shark.png')
    speed = 1

    def __init__(self, x = 30, y=30):
        super(Shark, self).__init__(image=Shark.image,
                                     x=x,
                                     y=y,
                                     dx=Shark.speed)

    def update(self):
        if self.right > games.screen.width:
            self.destroy()

    def handle_caught(self):
        self.destroy()


def main():
    games.music.load('music/song.mp3')

    games.music.play(-1)
    ocean_image = games.load_image('image/ocean.jpg', transparent=False)

    games.screen.background = ocean_image
    the_person = Person()
    games.screen.add(the_person)
    the_shark = Magic()
    games.screen.add(the_shark)
    games.mouse.is_visible = False

    games.screen.mainloop()


if __name__ == '__main__':
    main()