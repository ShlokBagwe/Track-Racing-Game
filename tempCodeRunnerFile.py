        player_collide_comp = player_car.collide(com_car,130,200)
        if player_collide_comp != None:
            player_car.bounce()
            computer_car.bounce()