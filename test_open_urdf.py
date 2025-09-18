import pybullet as p
import pybullet_data
import time

# Start the PyBullet GUI
physicsClient = p.connect(p.GUI)

# Set the path for PyBullet to find URDFs
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Reset simulation to a clean state
p.resetSimulation()

# Set gravity
p.setGravity(0, 0, -9.8)

# Load the ground plane
plane_id = p.loadURDF("plane.urdf")

# Load your URDF model (replace with your URDF filename if needed)
robot_id = p.loadURDF("/home/jennyw2/data/small_engine_on_table_2/small_engine_with_prismatic_cap2/urdf/small_engine_with_prismatic_cap2.urdf", basePosition=[0, 0, 0.34], useFixedBase=True)

# Keep the GUI running
while True:
    p.stepSimulation()
    time.sleep(1./240.)
