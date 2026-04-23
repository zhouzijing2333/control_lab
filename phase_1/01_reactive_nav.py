import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Obstacle:
    def __init__(self, x, y, radius):
        self.x, self.y = x, y
        self.radius = radius

class Robot:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.theta = 0
        self.speed = 0.8
        self.sensor_range = 6.0
        self.path_x = [x]
        self.path_y = [y]
        self.avoid_count = 0

    def move(self):
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)
        self.path_x.append(self.x)
        self.path_y.append(self.y)

    def detect_and_decide(self, obstacles):
        for obs in obstacles:
            dist = math.sqrt((self.x - obs.x)**2 + (self.y - obs.y)**2)
            if dist < self.sensor_range + obs.radius:
                self.avoid_count += 1
                # 避障逻辑：检测到障碍物，随机转向
                self.theta += random.uniform(0.5, 1.5)
                return True
        return False

# --- 初始化环境 ---
robot = Robot(0, 0)
obstacles = [Obstacle(random.uniform(10, 80), random.uniform(-20, 20), 2.5) for _ in range(15)]

# --- 设置绘图 ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-5, 100)
ax.set_ylim(-40, 40)
ax.set_aspect('equal')
ax.grid(True)

# 绘制障碍物
for obs in obstacles:
    circle = plt.Circle((obs.x, obs.y), obs.radius, color='red', alpha=0.6)
    ax.add_patch(circle)

# 机器人及其轨迹的绘图对象
line, = ax.plot([], [], 'b-', label='Trajectory', alpha=0.5)
robot_dot, = ax.plot([], [], 'go', markersize=8, label='Robot')
text_info = ax.text(0.02, 0.95, '', transform=ax.transAxes)
ax.legend()

def update(frame):
    # 逻辑更新
    robot.detect_and_decide(obstacles)
    robot.move()

    # 画面更新
    line.set_data(robot.path_x, robot.path_y)
    robot_dot.set_data([robot.x], [robot.y])
    text_info.set_text(f'Step: {frame} | Avoids: {robot.avoid_count} | Pos: ({robot.x:.1f}, {robot.y:.1f})')

    return line, robot_dot, text_info

# --- 启动动画 ---
# frames 为总步数，interval 为每帧间隔毫秒
ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True, repeat=False)

plt.title("Robot Obstacle Avoidance Simulation (Reactive Planning)")
plt.show()