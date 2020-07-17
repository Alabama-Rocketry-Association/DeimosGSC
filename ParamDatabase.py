import numpy as np

#dynamic model constants
gamma = 1.4				#ratio of specific heats for air
gasConst = 287			#gas constant for air (R)
refTemp = 291.15		#reference temperature (Kelvin) (Theta-naught)
dynVisc = 1.827e-7		#reference dynamic viscosity (Pa * s) (Mu-naught)
sutherland = 120		#Sutherland's constant (Kelvin) (C)
earthMass = 5.974e24	#mass of the Earth (Kg)
earthRad = 6378100		#radius of the Earth (m)
grav = 6.673e-11 		#universal gravitational constant (m^3 / kg * s)
yawRef = np.array([1, 0, ]) #reference yaw axis
pitchRef = np.array([0, 1, 0]) #reference pitch axis
rollRef = np.array([0, 0, 1]) # reference roll axis

	#position and orientation
		#necessary variables
			pitch = 	#rotation about *pitch* axis (radians)
			a_x = 		#acceleration???
			a_y = 
			a_z = 

s = cos(pitch / 2)
V_x = sin(pitch / 2) * a_x
V_y = sin(pitch / 2) * a_y
V_z = sin(pitch / 2) * a_z
velocity = np.array([V_x, V_y, V_z])	#a vector (ik it's an array we're gonna figure that out) containing the three dimensional velocities
	#Quaternion vector
		Quaternion[] = {s, V_x, V_y, V_z};

	#Quaternion to Rotation Matrix
		qRotation = np.array([
						[(1 - 2 * pow(V_y, 2) - 2 * pow(V_z, 2)), (2 * V_x * V_y - 2 * s * V_z), (2 * V_x * V_z + 2 * s * V_y)]
						[(2 * V_x * V_y + 2 * s * V_z), (1 - 2 * pow(V_x, 2) - 2 * pow(V_z, 2)), (2 * V_y * V_z - 2 * s * V_x)]
						[(2 * V_x * V_z - 2 * s * V_y), (2 * V_y * V_z + 2 * s * V_x), (1 - 2 * pow(V_x, 2) - 2 * pow(V_y, 2))]
					])

	#Reference inertia
		I_xx	#Moments of inertai about the rocket's yaw axis
		I_yy	#Moments of inertai about the rocket's pitch axis
		I_zz	#Moments of inertai about the rocket's roll axis

		#Reference inertia tensor

		inertiaTensor = np.array([[I_xx, 0, 0], [0, I_yy, 0], [0, 0, I_zz]])

	#Quaternion derivative
		s_dot = 0.50 * np.dot(angVelocity, velocity)
		v_dot = 0.50 * (s * angVelocity + np.cross(angVelocity, velocity))
