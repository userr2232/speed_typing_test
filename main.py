import pygame as pg
import sys
import os
from time import time

class ROAttrDict(dict):
    __getattr__ = dict.__getitem__

class Game:
    def __init__(self):
        self.caption = 'Speed Typing Test'
        self.title = 'Faster!'
        self.width, self.height = 800, 700
        self.dim = (self.width, self.height)
        self.input = ''
        self.accuracy = 0
        self.correct = 0
        self.total_words = 0
        self.written_words = 0
        self.total_time = 0
        self.wpm = 0
        self.running = False
        self.phrases = self.get_phrases()
        pg.init()
        self.image = pg.image.load('./static/images/typewriter.png')
        self.screen = pg.display.set_mode(self.dim)
        self.colors = {
            'BLACK': (0,0,0),
            'ORANGE': (255,94,19),
            'WHITE': (255,255,255),
            'GREEN': (146,227,111),
            'BLUE': (17,78,133),
            'LIGHT_BLUE': (84,160,231),
            'PINK': (245,32,99)
            }
        self.colors = ROAttrDict(self.colors)
        self.faster_font = self.get_font('FasterOne-Regular', 100)
        self.orbitron_font = self.get_font('Orbitron-VariableFont_wght', 20)
        self.final_score_font = self.get_font('Orbitron-VariableFont_wght', 80)
        pg.display.set_caption(self.caption)

    def get_font(self, font_name, size):
        dir = 'static/fonts'
        return pg.font.Font(os.path.join(dir, font_name + '.ttf'), size)

    def get_phrases(self):
        with open('./static/phrase-list.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def setup(self):
        self.screen.fill(self.colors.BLUE)
        rect_width = self.width - 100
        rect_height = 50
        pg.draw.rect(self.screen, self.colors.ORANGE, (
            int((self.width - rect_width) / 2),
            int((self.height - rect_height) / 2),
            rect_width,
            rect_height), 2)
        self.display_text(self.title, self.faster_font, self.colors.GREEN, 100)
        score_height = 390
        accuracy = self.orbitron_font.render('accuracy: {}%'.format(self.accuracy), True, self.colors.PINK)
        wpm = self.orbitron_font.render('wpm: {}'.format(self.wpm), True, self.colors.PINK)
        self.screen.blit(accuracy, (
            int((self.width - rect_width) / 2),
            score_height))
        self.screen.blit(wpm, (
            int((self.width - rect_width) / 2) + accuracy.get_rect().width + 20,
            score_height))

    def finish(self):
        self.screen.fill(self.colors.BLUE)
        self.display_text('Finished!', self.faster_font, self.colors.GREEN, 100)
        self.display_text('accuracy: {}'.format(self.accuracy), self.final_score_font, self.colors.PINK, 250)
        self.display_text('wpm: {}'.format(self.wpm), self.final_score_font, self.colors.PINK, 350)


    def display_text(self, text, font, color, y_pos):
        text = font.render(text, True, color)
        self.screen.blit(text, (
            int((self.width - text.get_rect().width) / 2),
            y_pos
        ))

    def update_stats(self, phrase, input_text, time):
        phrase_words = phrase.split()
        input_words = input_text.split()
        self.written_words += len(input_words)
        self.total_words += len(phrase_words)
        self.total_time += time
        for word in input_words:
            if word in phrase_words:
                self.correct += 1
            else:
                self.correct -= 0.5
        self.correct = self.correct if self.correct >= 0 else 0
        self.accuracy = round(self.correct / self.total_words * 100, 2)
        self.wpm = round(self.written_words / self.total_time * 60)

    def check_quit(self, event):
        if event.type == pg.QUIT:
            self.running = False
            pg.quit()
            sys.exit()

    def run(self):
        self.running = True
        for phrase in self.phrases:
            input_text = ''
            completed = False
            start = time()
            while self.running and not completed:
                self.setup()
                self.display_text(phrase, self.orbitron_font, self.colors.WHITE, 250)
                for event in pg.event.get():
                    self.check_quit(event)
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            input_text = input_text[:-1]
                        if event.key == pg.K_RETURN:
                            end = time()
                            completed = True
                            self.update_stats(phrase, input_text, end-start)
                        else:
                            input_text += event.unicode
                self.display_text(input_text, self.orbitron_font, self.colors.WHITE, 337)
                pg.display.update()
        self.finish()
        pg.display.update()
        while self.running:
            for event in pg.event.get():
                self.check_quit(event)

Game().run()