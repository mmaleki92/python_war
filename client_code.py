import war_game
from war_game import Builder

def main():
    war = war_game.War()
    build = Builder()

    wall = build.wall(100, 100, 10, 10, False, "wall")
    war.add_equip([wall])
    war.start()

if __name__ == "__main__":
    main()