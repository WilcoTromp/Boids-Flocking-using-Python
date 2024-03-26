import random
import math
import pygame
from Vector import *

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

class Boid:
    def __init__(self, x, y, color):
        self.color = color
        self.position = Vector(x, y)
        vec_x = random.uniform(-1, 1)
        vec_y = random.uniform(-1, 1)
        self.velocity = Vector(vec_x, vec_y)
        self.velocity.normalize()

        self.velocity = self.velocity * random.uniform(1, 2.5)
        self.acceleration = Vector()
        self.max_speed = 2
        self.max_length = 1
        self.radius = 50
        self.angle = 0

        self.toggles = {"separation":True, "alignment":True, "cohesion":True}
        self.values = {"separation":0.1, "alignment":0.1, "cohesion":0.1}

    def limits(self, width, height):
        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width

        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height

    def behaviour(self, flock):
        self.acceleration.reset()

        if self.toggles["separation"] == True:
            avoid = self.separation(flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)

        if self.toggles["cohesion"] == True:
            coh = self.cohesion(flock)
            coh = coh * self.values["cohesion"]
            self.acceleration.add(coh)

        if self.toggles["alignment"] == True:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)

    def separation(self, group):
        total = 0
        steering = Vector()

        for member in group:
            distance = getDistance(self.position, member.position)
            if member != self and distance < self.radius:
                temp = SubVectors(self.position, member.position)
                temp = temp/(distance ** 2)
                steering.add(temp)
                total += 1

        if total > 0:
            steering = steering / total
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            steering.limit(self.max_length)

        return steering

    def alignment(self, group):
        total = 0
        steering = Vector()

        for member in group:
            distance = getDistance(self.position, member.position)
            if member != self and distance < self.radius:
                if member.color == self.color:
                    velocity = member.velocity.Normalize()
                    steering.add(velocity)
                    total += 1
                else:
                    temp = SubVectors(self.position, member.position)
                    temp = temp / (distance ** 2)
                    steering.add(temp)
                    total += 1

        if total > 0:
            steering = steering / total
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity.Normalize()
            steering.limit(self.max_length)
        return steering

    def cohesion(self, group):
        total = 0
        steering = Vector()

        for member in group:
            distance = getDistance(self.position, member.position)
            if member != self and distance < self.radius:
                steering.add(member.position)
                total += 1

        if total > 0:
            steering = steering / total
            steering = steering - self.position
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            steering.limit(self.max_length)

        return steering

    def update(self, dots):
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit(self.max_speed)
        self.angle = self.velocity.heading() + math.pi / 2

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), 5)

class Predator:
    def __init__(self, x, y, color):
        self.position = Vector(x, y)
        vec_x = random.uniform(-1, 1)
        vec_y = random.uniform(-1, 1)
        self.velocity = Vector(vec_x, vec_y)
        self.velocity.normalize()
        self.velocity = self.velocity * random.uniform(3, 4)
        self.acceleration = Vector()

        self.max_speed = 3
        self.max_length = 1
        self.angle = 0
        self.radius = 40
        self.color = color

        self.toggles = {"separation": True, "alignment": True, "cohesion": True}
        self.values = {"separation": 0.1, "alignment": 0.1, "cohesion": 0.1}

    def limits(self, width, height):
        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width

        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height

    def behaviour(self, flock):
        self.acceleration.reset()

        if self.toggles["separation"] == True:
            avoid = self.separation(flock)
            avoid = avoid * self.values["separation"]
            self.acceleration.add(avoid)

        if self.toggles["cohesion"] == False:
            coh = self.cohesion(flock)
            coh = coh * self.values["cohesion"]
            self.acceleration.add(coh)

        if self.toggles["alignment"] == False:
            align = self.alignment(flock)
            align = align * self.values["alignment"]
            self.acceleration.add(align)

    def separation(self, group):
        total = 0
        steering = Vector()

        for member in group:
            distance = getDistance(self.position, member.position)
            if member != self and distance < self.radius:
                temp = SubVectors(self.position, member.position)
                temp = temp / (distance ** 2)
                steering.add(temp)
                total += 1

        if total > 0:
            steering = steering / total
            steering.normalize()
            steering = steering * self.max_speed
            steering = steering - self.velocity
            steering.limit(self.max_length)

        return steering

    def alignment(self, group):
        pass

    def cohesion(self, group):
        pass

    def update(self, dots):
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity.limit(self.max_speed)
        self.angle = self.velocity.heading() + math.pi / 2

        for dot in dots:
            if dot != self:
                distance = math.sqrt((self.position.x - dot.position.x) ** 2 + (self.position.y - dot.position.y) ** 2)
                if distance < 50 and dot.color == (255, 192, 203):
                    dx = self.position.x - dot.position.x
                    dy = self.position.y - dot.position.y
                    length = math.sqrt(dx ** 2 + dy ** 2)
                    if length > 0:
                        dx /= length
                        dy /= length
                    angle_to_dot = math.atan2(dot.position.y - self.position.y, dot.position.x - self.position.x)
                    avoidance_angle = angle_to_dot - math.pi
                    self.angle += (avoidance_angle - self.angle) * 0.1

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), 7.5)

class Obstacle:
    def __init__(self, x, y, color, dot_radius):
        self.position = Vector(x, y)
        self.color = color
        self.radius = dot_radius
        self.velocity = Vector(0,0)

    def limits(self, width, height):
        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width

        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height

    def behaviour(self, flock):
        pass

    def separation(self, group):
        pass

    def alignment(self, group):
        pass

    def cohesion(self, group):
        pass

    def update(self, other_dots):
        pass

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), int(self.radius))