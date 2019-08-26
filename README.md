# bowlingscorer

REST API that provides all the necessary calls needed to run a game of bowling

# Tools Used

Python 3.6
Flask (Code from https://flask.palletsprojects.com/en/1.1.x/tutorial/ is used)
Pytest

# Calls Available

create_game
delete_game
add_player
delete_player
add_frame
update_frame
get_score
get_frame_info

# Tests

test_create_delete_game
test_create_delete_player
test_add_player_failures
test_delete_game_failures
test_delete_player_failures
test_add_frame
test_add_frame_failures
test_update_frame
test_update_frame_failures
test_perfect_game
test_spare
test_get_score
test_get_score_failures
test_get_frame_info
test_get_frame_info_failures