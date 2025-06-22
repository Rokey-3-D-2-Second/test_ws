# gripper_action_server.py
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer

from control_msgs.action import GripperCommand
from sensor_msgs.msg import JointState

from .onrobot import RG  # 기존 Modbus 제어 코드 import

class GripperActionServer(Node):
    GRTIPPER_NAME = 'rg2'
    TOOLCHARGER_IP = '192.168.1.1'
    TOOLCHARGER_PORT = '502'

    def __init__(self):
        super().__init__('gripper_action_server')
        self.gripper = RG(self.GRTIPPER_NAME, self.TOOLCHARGER_IP, self.TOOLCHARGER_PORT)  # IP/PORT 맞게 수정
        self.current_width = 0.0  # mm 단위

        self._action_server = ActionServer(
            self,
            GripperCommand,
            'gripper_controller/gripper_command',  # MoveIt에서 찾는 action_ns에 맞춤
            self.execute_callback
        )
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)

        # 10Hz로 상태 publish
        self.create_timer(0.1, self.publish_joint_state)

    def execute_callback(self, goal_handle):
        width = goal_handle.request.command.position * 1000  # m → mm 변환
        force = goal_handle.request.command.max_effort if goal_handle.request.command.max_effort > 0 else 400
        self.gripper.move_gripper(int(width), int(force))
        self.current_width = width
        
        goal_handle.succeed()

        result = GripperCommand.Result()
        result.position = goal_handle.request.command.position
        result.effort = goal_handle.request.command.max_effort
        result.stalled = False
        result.reached_goal = True
        return result
    
    def publish_joint_state(self):
        width_m = float(self.current_width) / 1000.0 # mm → m 변환
        
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = ['rg2_finger_joint1', 'rg2_finger_joint2']
        js.position = [width_m, width_m]
        
        self.joint_pub.publish(js)

def main(args=None):
    rclpy.init(args=args)
    node = GripperActionServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()