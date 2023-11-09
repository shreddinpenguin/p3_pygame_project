from relationships import *
# from game import *
import inquirer
import time
from level import *
from prints import *
from sys import exit
from player import *
from settings import *
import pygame
import math
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# level = Level(level_map, screen)
# globalScore = 0
def run_game():
    
    pygame.init()
    # def display_score():
    #     font = pygame.font.SysFont('Arial', 40)
    #     current = int(pygame.time.get_ticks() / 2000)
    #     score_surf = font.render(str(points), True, "black")
    #     score_rect = score_surf.get_rect(midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10))
    #     screen.blit(score_surf,score_rect)
    #     return current

    #setting screen size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    level = Level(level_map, screen)
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen_rect = screen.get_rect()
    #framerate
    FPS = 60
    pygame.display.set_caption('Flap.py')
    clock = pygame.time.Clock()
    # level = Level(level_map, screen)
    points = 0
    globalScore = level.display_score()
    print(globalScore)
    #background load & scroll
    bg = pygame.image.load("lib/images/cloud-bg.jpeg").convert()
    bg_width = bg.get_width()
    scroll = 0
    panes = math.ceil(SCREEN_HEIGHT / bg_width) + 1
    #game loop
    run = True
    
    while run:
        #setting FPS
        clock.tick(FPS)
        #Background scroll
        for i in range(0, panes):
            screen.blit(bg, (i * bg_width + scroll, 0))
        scroll -= 0.5
        if abs(scroll) > bg_width:
            scroll = 0
        level.run()
        # points = display_score()
        points = level.points
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
    pygame.quit()
    return points

def main_menu():
    time.sleep(1)
    print_flappy()
    print(Level)
    main_menu = [
        inquirer.List('option',
            message='Please Select',
            choices=['Play Now', 'High Scores', 'Delete Player', 'Exit'],
        ),
    ]
    main_menu_answers = inquirer.prompt(main_menu)
    main_menu_answers_key = main_menu_answers['option']
    if main_menu_answers_key == 'Play Now':
        player_menu()
    elif main_menu_answers_key == 'High Scores':
        # high_score()
        pass
    elif main_menu_answers_key == 'Delete Player':
        delete_player()
    elif main_menu_answers_key == 'Exit':
        print_goodbye()
        exit()
        
def player_menu():   
    players = session.query(User).all()
    select_player = [
        inquirer.List('player_opt',
            message="Are you a new or existing player?",
            choices=['New','Exisiting'],
        ),
    ]
    select_player_answer = inquirer.prompt(select_player)
    select_player_answer_key = select_player_answer['player_opt']
    if select_player_answer_key == 'New':
        create_new_player()
    if select_player_answer_key == 'Exisiting':
        if not players:
            print('Sorry No Exsisting Users')
        else:
            existing_user()

def create_new_player():
        player_names = session.query(User.name).all()
        question = [
            inquirer.Text('name', message='Enter Your Name'),
        ]
        answers = inquirer.prompt(question)
        new_player = User(
            name = answers['name'],
        )
        if new_player.name in [player[0] for player in player_names]:
            print('Name is already in use')
            create_new_player()
        else:
            session.add(new_player)
            session.commit()
            player1 = session.query(User).filter_by(name = new_player.name).first()
            run_game()
            final_score = globalScore
            print(final_score)
            # print(final_score)
            new_result = Result(
                player_name = new_player.name,
                score = final_score,
                user_id = new_player.id
            )
            session.add(new_result)
            session.commit()
            main_menu()
        
def existing_user():
    users = session.query(User).all()
    user_list = [
        inquirer.List('player_list',
            message="Select an Exsisting Player",
            choices=[user.name for user in users],
        ),
    ]
    answer = inquirer.prompt(user_list)
    answer_key = answer['player_list']
    print(answer_key)
    run_game()
    final_score = globalScore
    print(final_score)
    new_result = Result(
        player_name = answer_key.name,
        score = final_score
    )
    print_game_over()
    session.add(new_result)
    session.commit()
    main_menu()

# def high_score():
#     players = session.query(Player).all()
#     all_scores = session.query(Result).all()
#     all_score_scores = [(score.score,score.players.name) for score in all_scores]
#     sortedlist = sorted(all_score_scores, key=lambda k: k[0], reverse=True)
#     if not players:
#             print('Sorry No Exsisting Users')
#     else:
#         print(r'''

#  _    _ _       _        _____                         
# | |  | (_)     | |      / ____|                        
# | |__| |_  __ _| |__   | (___   ___ ___  _ __ ___  ___ 
# |  __  | |/ _` | '_ \   \___ \ / __/ _ \| '__/ _ \/ __|
# | |  | | | (_| | | | |  ____) | (_| (_) | | |  __/\__ \
# |_|  |_|_|\__, |_| |_| |_____/ \___\___/|_|  \___||___/
#            __/ |                                       
#           |___/                                        

# 1) {sortedlist[0][0]} // Set By: {sortedlist[0][1]}
# 2) {sortedlist[1][0]} // Set By: {sortedlist[1][1]}                                                                                
# 3) {sortedlist[2][0]} // Set By: {sortedlist[2][1]}                                                                                
#             ''')

def delete_player():
    players = session.query(User).all()
    question = [
        inquirer.List('delete',
            message="Select a Player",
            choices=[player.name for player in players] + ['Back'],
        ),
    ]
    answer = inquirer.prompt(question)
    if answer['delete'] == 'Back':
        main_menu()
    else:
        question2 = [
            inquirer.List('confirm',
                message='Delete Player?',
                choices= ['Yes', 'No']
            ),
        ]
        answer2 = inquirer.prompt(question2)
        if answer2['confirm'] == 'No':
            print('User will not be deleted')
        if answer2['confirm'] == 'Yes':
            print(answer)
            player = session.delete(session.query(User).filter_by(name = answer["delete"]).first())
            session.commit()        
            print('User Deleted')
        main_menu()


main_menu()
