from controller import Supervisor, Emitter

TIME_STEP = 64
GAME_TIME = 10 * 60 * 1000  # Game duration in milliseconds
GOAL_X_LIMIT = 0.75  # X-coordinate beyond which a goal is scored

supervisor = Supervisor()
emitter = supervisor.getDevice('emitter')

ball_node = supervisor.getFromDef('BALL')

scores = {"B": 0, "Y": 0}

while supervisor.step(TIME_STEP) != -1:
    if supervisor.getTime() > GAME_TIME / 1000.0:
        break

    ball_position = ball_node.getPosition()
    if ball_position[0] > GOAL_X_LIMIT:
        scores["B"] += 1
    elif ball_position[0] < -GOAL_X_LIMIT:
        scores["Y"] += 1

    if abs(ball_position[0]) > 1 or abs(ball_position[2]) > 1:
        continue

print("Final scores:")
print("Blue: ", scores["B"])
print("Yellow: ", scores["Y"])
