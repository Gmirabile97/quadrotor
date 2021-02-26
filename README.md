# quadrotor
I comandi da runnare sono questi due. Uno spawna mondo su gazebo, quadrotor e rviz. L'altro inizia il decollo e tutta la pianificazione con esecuzione.

roslaunch hector_moveit_gazebo orchyard_navigation.launch

roslaunch hector_moveit_exploration_mod explore.launch


Il drone si trova in:

hector_quadrotor/hector_quadrotor_description/urdf/quadrotor_with_kinect.urdf.xacro

I plugin si trovano in:

hector_quadrotor/hector_quadrotor_gazebo/urdf/

Il pacchetto generato dal MoveIt assistant è hector_moveit_config_mod che può essere modificato eseguendo setup_assistant.launch

In hector_moveit_esploration_mod si trova l'esplorazione del drone con decollo, pianificazione, esecuzione, atterraggio
