from relationships import *
import inquirer
import time
from prints import *
from sys import exit
from game import *

def main_menu():
    time.sleep(1)
    print_flappy()
    main_menu = [
        inquirer.List('option',
            message='Please Select',
            choices=['Play Now', 'High Scores', 'Edit Player', 'Exit'],
        ),
    ]
    main_menu_answers = inquirer.prompt(main_menu)
    main_menu_answers_key = main_menu_answers['option']
    if main_menu_answers_key == 'Play Now':
        player_menu()
    elif main_menu_answers_key == 'High Scores':
        high_score()
    elif main_menu_answers_key == 'Edit Player':
        edit_player()
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
            player_menu()
        else:
            existing_user()

def create_new_player():
    global globalScore
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
        print("past game running")
        new_result = Result(
            player_name = new_player.name,
            score = globalScore,
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
    main_menu()
    print("end of existing player")
    # final_score = globalScore
    print(globalScore)
    new_result = Result(
        player_name = answer_key.name,
        score = globalScore
    )
    print_game_over()
    session.add(new_result)
    session.commit()
    

def high_score():
    players = session.query(User).all()
    all_scores = session.query(Result).all()
    all_score_scores = [(score.score,score.player_name) for score in all_scores]
    sortedlist = sorted(all_score_scores, key=lambda k: k[0], reverse=True)
    if not players:
        print('Sorry No Exsisting Users')
    else:
        print(f'''
 _    _ _       _        _____                         
| |  | (_)     | |      / ____|                        
| |__| |_  __ _| |__   | (___   ___ ___  _ __ ___  ___ 
|  __  | |/ _` | '_ \   \___ \ / __/ _ \| '__/ _ \/ __|
| |  | | | (_| | | | |  ____) | (_| (_) | | |  __/\__ \\
|_|  |_|_|\__, |_| |_| |_____/ \___\___/|_|  \___||___/
           __/ |                                       
          |___/                                        

1) {sortedlist[0][1]}: {sortedlist[0][0]}
2) {sortedlist[1][1]}: {sortedlist[1][0]}                                                                             
3) {sortedlist[2][1]}: {sortedlist[2][0]}                                                                               
        ''')
    main_menu()

def edit_player():
    player_menu = [
        inquirer.List('option',
            message='Please Select',
            choices=['Edit Player Name', 'Delete a Player', 'Back'],
        ),
    ]
    player_menu_answers = inquirer.prompt(player_menu)
    player_menu_answers_key = player_menu_answers['option']
    if player_menu_answers_key == 'Edit Player Name':
        edit_name()
    elif player_menu_answers_key == 'Delete a Player':
        delete_player()
    elif player_menu_answers_key == 'Back':
        main_menu()

def edit_name():
    players = session.query(User.name).all()
    query = [
        inquirer.List('edit',
            message="Select a Player to Edit",
            choices=[player.name for player in players] + ['Back'],
        ),
    ]
    answer = inquirer.prompt(query)
    if answer['edit'] == 'Back':
        edit_player()
    else:
        question = [
            inquirer.Text('name', message='Change Name'),
        ]
        answer2 = inquirer.prompt(question)
        player = session.query(User).filter_by(name=answer['edit']).first()
        if not player:
            print('Player does not exist.')
            edit_name()
        # answer_player = answer['edit']
        player.name = answer2['name']
        session.commit()        
        print('Name Changed')
        time.sleep(1)
        edit_name()

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
        edit_player()
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
            time.sleep(1)
        delete_player()


main_menu()
