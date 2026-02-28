import arcade

from arcade.particles import FadeParticle, Emitter, EmitBurst
from random import choice, uniform


def player_appearance(x, y, count=200):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=arcade.make_circle_texture(6, arcade.color.WHITE),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 100.0),
            lifetime=uniform(1, 2),
            scale=1,
            mutation_callback=gravity_drag,
        ),
    )


def player_explosion(x, y, count=100):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=arcade.make_circle_texture(6, arcade.color.WHITE),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 10.0),
            lifetime=uniform(1, 2),
            scale=1,
            mutation_callback=gravity_drag,
        ),
    )


def make_explosion(x, y, count=80):
    RAINBOW_COLORS = (
        arcade.color.ELECTRIC_CRIMSON,
        arcade.color.FLUORESCENT_ORANGE,
        arcade.color.ELECTRIC_YELLOW,
        arcade.color.ELECTRIC_GREEN,
        arcade.color.ELECTRIC_CYAN,
        arcade.color.MEDIUM_ELECTRIC_BLUE,
        arcade.color.ELECTRIC_INDIGO,
        arcade.color.ELECTRIC_PURPLE,
    )
    SPARK_TEX = [arcade.make_circle_texture(6, clr) for clr in RAINBOW_COLORS]

    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 50.0),
            lifetime=0.5,
            scale=1,
            mutation_callback=gravity_drag,
        ),
    )


def gravity_drag(p):  # Для искр: чуть вниз и затухание скорости
    p.change_y += -0.03
    p.change_x *= 0.92
    p.change_y *= 0.92
