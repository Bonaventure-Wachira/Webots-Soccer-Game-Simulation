from controller import Robot, Motor, PositionSensor, Receiver
import random

TIME_STEP = 64
MAX_SPEED = 6.28
GAME_TIME = 10 * 60  # in seconds

last_direction_change_time = 0

def set_motor_speeds(left_speed, right_speed):
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

def initialize_robot():
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)
    left_sensor.enable(TIME_STEP)
    right_sensor.enable(TIME_STEP)
    receiver.enable(TIME_STEP)

def process_receiver_data():
    message = receiver.getString()
    
    if message != 'RESET':
        ball_x, ball_y = map(float, message.split())
        
        global last_direction_change_time
        if robot.getTime() - last_direction_change_time > 10 * TIME_STEP / 1000.0:
            direction = random.choice([-1, 1])
            last_direction_change_time = robot.getTime()
            if direction > 0:
                set_motor_speeds(MAX_SPEED, MAX_SPEED / 2)
            else:
                set_motor_speeds(MAX_SPEED / 2, MAX_SPEED)

def main():
    initialize_robot()
    while robot.step(TIME_STEP) != -1:
        if robot.getTime() > GAME_TIME:
            set_motor_speeds(0, 0)
            break
        if receiver.getQueueLength() > 0:
            process_receiver_data()
            receiver.nextPacket()
        else:
            set_motor_speeds(MAX_SPEED / 2, MAX_SPEED)

if __name__ == "__main__":
    robot = Robot()
    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")
    left_sensor = robot.getDevice("left wheel sensor")
    right_sensor = robot.getDevice("right wheel sensor")
    receiver = robot.getDevice("receiver")
    main()
