
import tkinter as tk
from random import randint, choice
from tkinter import messagebox

class BalloonGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Balloon Pop Game")
        self.canvas_width = 600
        self.canvas_height = 600
        self.score = 0
        self.lives = 5
        self.balloons = []
        self.colors = ['red', 'blue', 'green', 'yellow', 'purple']
        self.balloon_speed = 30  
        self.spawn_delay = 1000  # new balloon  (in ms)
        
        self.create_ui()
        self.root.after(self.spawn_delay, self.spawn_balloon)
        self.root.after(self.balloon_speed, self.move_balloons)
        

    def create_ui(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # set background image
        self.bg_image = tk.PhotoImage(file="balloon blast.png")
        self.canvas.create_image(0, 0, image=self.bg_image, anchor='nw')

        # score and lives display
        self.score_text = self.canvas.create_text(10, 10, anchor='nw', font=('Arial', 16), fill='white', text='Score: 0')
        self.lives_text = self.canvas.create_text(self.canvas_width - 10, 10, anchor='ne', font=('Arial', 16), fill='white', text='Lives: 5')

    def spawn_balloon(self):
        x = randint(50, self.canvas_width - 50)
        size = randint(30, 50)
        color = choice(self.colors)
        balloon = self.canvas.create_oval(x, self.canvas_height, x + size, self.canvas_height + size, fill=color, outline='')
        self.balloons.append((balloon, size))
        self.canvas.tag_bind(balloon, '<Button-1>', self.pop_balloon)
        self.root.after(randint(800, 1500), self.spawn_balloon)

    def move_balloons(self):
        for balloon, size in self.balloons[:]:
            self.canvas.move(balloon, 0, -5)  # -5 means move upward
            coords = self.canvas.coords(balloon)
            if coords and coords[1] <= 0:
                self.canvas.delete(balloon)
                self.balloons.remove((balloon, size))
                self.lives -= 1
                self.canvas.itemconfigure(self.lives_text, text=f'Lives: {self.lives}')
                if self.lives == 0:
                    self.end_game()
        self.root.after(self.balloon_speed, self.move_balloons)

    def pop_balloon(self, event):
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        for balloon, size in self.balloons:
            if balloon == clicked_item:
                self.canvas.delete(balloon)
                self.balloons.remove((balloon, size))
                self.score += 1
                self.canvas.itemconfigure(self.score_text, text=f'Score: {self.score}')
                break

    def end_game(self):
        if messagebox.askyesno("Game Over", f"Final Score: {self.score}\nPlay Again?"):
            self.restart_game()
        else:
            self.root.destroy()

    def restart_game(self):
        self.score = 0
        self.lives = 5
        for balloon, _ in self.balloons:
            self.canvas.delete(balloon)
        self.balloons.clear()
        self.canvas.itemconfigure(self.score_text, text='Score: 0')
        self.canvas.itemconfigure(self.lives_text, text='Lives: 5')
        self.root.after(self.spawn_delay, self.spawn_balloon)

if __name__ == "__main__":
    root = tk.Tk()
    game = BalloonGame(root)
    root.mainloop()
