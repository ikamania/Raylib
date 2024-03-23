import pyray as pr
import random as rn


class App:
    def __init__(self) -> None:
        self.W, self.H = 800, 450
        self.GROUND = 75
        self.SCORE = 0

        self.x, self.y = 100, 0

        self.enemys = [[1000, self.H - self.GROUND - 25, 25, 25]]

    def draw_player(self) -> None:
        y = self.H - self.y - 25 - self.GROUND

        pr.draw_circle_v((self.x, y), 25, pr.BLACK)
        pr.draw_circle_v((self.x - 10, y), 5, pr.WHITE)
        pr.draw_circle_v((self.x + 10, y), 5, pr.WHITE)

    def draw_ground(self) -> None:
        pr.draw_line(0, self.H - self.GROUND, self.W, self.H - self.GROUND, pr.WHITE)

    def draw_score(self) -> None:
        pr.draw_text(f"{self.SCORE}", 10, 10, 50, pr.PINK)

    def generate_enemy(self) -> None:
        w, h = rn.randint(15, 100), rn.randint(15, 50)

        x, y = rn.randint(0, 500) + self.W, self.H - self.GROUND - h

        self.enemys.append([x, y, w, h])

    def run(self) -> None:
        pr.init_window(self.W, self.H, "DINO")
        pr.set_target_fps(60)

        ALIVE = True

        jump = False
        timer = 0

        while not pr.window_should_close() and ALIVE:
            if pr.is_key_pressed(pr.KEY_SPACE) and self.y == 0:
                jump = True

            if jump:
                self.y += 30

                if self.y >= 200:
                    jump = False

            if self.y != 0:
                self.y -= 10
            
            if timer >= rn.randint(80, 100):
                self.generate_enemy()

                timer = 0

            # DRAW
            pr.begin_drawing()
            pr.clear_background(pr.GRAY)

            self.draw_player()
            self.draw_ground()
            self.draw_score()

            for enemy in self.enemys:
                if enemy[0] < -100:
                    self.enemys.remove(enemy)
                    self.SCORE += 1
                else:
                    enemy[0] -= 10 + int(self.SCORE / 10)

                pl_rect = pr.Rectangle(self.x, self.H - self.y - 25 - self.GROUND, 25, 25)
                en_rect = pr.Rectangle(*enemy)
                
                if pr.check_collision_recs(pl_rect, en_rect):
                    ALIVE = False

                pr.draw_rectangle_rec(enemy, pr.WHITE)

            pr.end_drawing()

            timer += 1

        pr.close_window()
