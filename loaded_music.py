import arcade


sequence = arcade.load_sound('sfx/sequence.mp3')  # level playing music

ship_explode = arcade.load_sound('sfx/ship_explode.wav')
enemy_explode = arcade.load_sound("sfx/enemy_explode.wav")

bomb_activated = arcade.load_sound("sfx/bomb.wav")
bomb_pickup = arcade.load_sound('sfx/pickup_smartbomb.wav')

game_over = arcade.load_sound('sfx/game_over.wav')
fire = arcade.load_sound("sfx/fire.wav")
bullet_hitwall = arcade.load_sound("sfx/bullet_hitwall.wav")
shield_off = arcade.load_sound('sfx/shield_off.wav')
