# python chess
 Chess game created with Python and Pygame
By 000Nobody 

Added q_learning for chess (not fast at all) as a school project
it really needs optimalization
i had to change and add some functions in given classes i hope i didnt ruin the original game.

How to use:
1. open training.py
2. set starting_q_table to None (if u already have trained with this program you can just copy paste the file name to impove it).
3. all boards list has to be empty ([]).
4. set your number of games (HM_EPISODES) and number of turns (in function if turn ==...) you can also set SHOW_EVERY costatnt to see the games being played.
5. you can also change values for learning rate(LEARNING_RATE), discount (DISCOUNT) and epsilon (epsilon) values, but i dont recomend doing it if you dont know, what these values mean.
6. run the file to create your own q_table and all_boards list. IT TAKES A WHILE
7. for using your created AI in the game open human_vs_AI.py
8. copy paste name of your q_table(q_table) and all_boards(boards_save) list. (their names have to match except the "boards" and "q_table")
9. run the file and play the game. (you have to wait for a while to load all boards)

At the end i would like to thank for the original game. It needs the improvement too but it is the best free to use chess engine i have found.
