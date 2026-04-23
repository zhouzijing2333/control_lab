import math
import random


class Obstacle:
    def __init__(self, x, y, radius):
        self.x, self.y = x, y
        self.radius = radius


class Robot:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.theta = 0  # 朝向角度
        self.speed = 1.0
        self.sensor_range = 5.0  # 探测距离
        self.path = []  # 存储轨迹点
        self.avoid_count = 0  # 避障触发计数

    def move(self):
        # 基础运动学模型
        self.x += self.speed * math.cos(self.theta)
        self.y += self.speed * math.sin(self.theta)
        self.path.append((self.x, self.y))

    def detect_and_decide(self, obstacles):
        """
        核心决策规划逻辑 (Decision & Planning)
        """
        for obs in obstacles:
            # 计算机器人与障碍物的距离
            dist = math.sqrt((self.x - obs.x) ** 2 + (self.y - obs.y) ** 2)

            # 如果进入感知范围
            if dist < self.sensor_range + obs.radius:
                self.avoid_count += 1  # 计数：触发避障逻辑
                print(f"检测到碰撞风险！执行避障转向... (次数: {self.avoid_count})")

                # 简单的势场法思想：向相反方向转向
                self.theta += math.pi / 4  # 转向 45 度
                return True
        return False


# --- 模拟运行 ---
robot = Robot(0, 0)
obstacles = [Obstacle(random.uniform(5, 50), random.uniform(-10, 10), 2) for _ in range(10)]

for step in range(50):
    robot.detect_and_decide(obstacles)
    robot.move()
    print(f"Step {step}: Pos({robot.x:.1f}, {robot.y:.1f}), Avoids: {robot.avoid_count}")