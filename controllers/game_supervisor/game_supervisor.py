from controller import Supervisor, Emitter
import random

TIME_STEP = 64
GAME_TIME = 10 * 60 * 1000  # Game duration in milliseconds
GOAL_X_LIMIT = 0.75

INITIAL_ROBOT_POSITIONS = {
    "B1": [0.2, 0, 0.3],
    "B2": [-0.2, 0, 0.3],
    "Y1": [0.2, 0, -0.3],
    "Y2": [-0.2, 0, -0.3],
}
INITIAL_BALL_POSITION = [0, 0, 0]

supervisor = Supervisor()
emitter = supervisor.getDevice('emitter')

robot_nodes = {}
for robot_name in INITIAL_ROBOT_POSITIONS.keys():
    robot_nodes[robot_name] = supervisor.getFromDef(robot_name)
ball_node = supervisor.getFromDef('BALL')

def reset_positions():
    for robot_name, robot_node in robot_nodes.items():
        translation_field = robot_node.getField('translation')
        translation_field.setSFVec3f(INITIAL_ROBOT_POSITIONS[robot_name])
       
        rotation_field = robot_node.getField('rotation')
        rotation_field.setSFRotation([0, 1, 0, random.uniform(-3.14, 3.14)])

    ball_translation_field = ball_node.getField('translation')
    ball_translation_field.setSFVec3f(INITIAL_BALL_POSITION)

    emitter.send("RESET".encode('utf-8'))

scores = {"B": 0, "Y": 0}

while supervisor.step(TIME_STEP) != -1:
    if supervisor.getTime() > GAME_TIME / 1000.0:
        break

    ball_position = ball_node.getPosition()
    if ball_position[0] > GOAL_X_LIMIT:
        scores["B"] += 1
        reset_positions()
    elif ball_position[0] < -GOAL_X_LIMIT:
        scores["Y"] += 1
        reset_positions()

    if abs(ball_position[0]) > 1 or abs(ball_position[2]) > 1:
        reset_positions()

print("Final scores:")
print("Blue: ", scores["B"])
print("Yellow: ", scores["Y"])
