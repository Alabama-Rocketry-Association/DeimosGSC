	//dynamic model constants
double gamma = 1.4;		//ratio of specific heats for air
double gasConst = 287;	//gas constant for air (R)
double refTemp = 291.15; //reference temperature (Kelvin) (Theta-naught)
double dynVisc = 1.827e-7; //reference dynamic viscosity (Pa * s) (Mu-naught)
double sutherland = 120; //Sutherland's constant (Kelvin) (C)
double earthMass = 5.974e24; //mass of the Earth (Kg)
double earthRad = 6378100; //radius of the Earth (m)
double grav = 6.673e-11; //universal gravitational constant (m^3 / kg * s)
double yawRef[] = {1, 0, 0}; //reference yaw axis
double pitchRef[] = {0, 1, 0}; //reference pitch axis
double rollRef[] = {0, 0, 1}; // reference roll axis

	//position and orientation
		//necessary variables
			double pitch;	//rotation about *pitch* axis (radians)
			double a_x;		//acceleration???
			double a_y;
			double a_z;

double s = cos(pitch / 2)
double V_x = sin(pitch / 2) * a_x;
double V_y = sin(pitch / 2) * a_y;
double V_z = sin(pitch / 2) * a_z;
double velocity[] = {V_x, V_y, V_z};	//a vector (ik it's an array we're gonna figure that out) containing the three dimensional velocities
	//Quaternion vector
		double Quaternion[] = {s, V_x, V_y, V_z};

	//Quaternion to Rotation Matrix
		double Rotation[] = {
							{(1 - 2 * pow(V_y, 2) - 2 * pow(V_z, 2)), (2 * V_x * V_y - 2 * s * V_z), (2 * V_x * V_z + 2 * s * V_y)}
							{(2 * V_x * V_y + 2 * s * V_z), (1 - 2 * pow(V_x, 2) - 2 * pow(V_z, 2)), (2 * V_y * V_z - 2 * s * V_x)}
							{(2 * V_x * V_z - 2 * s * V_y), (2 * V_y * V_z + 2 * s * V_x), (1 - 2 * pow(V_x, 2) - 2 * pow(V_y, 2))}
							};

	//Reference inertia
		double I_xx;	//Moments of inertai about the rocket's yaw axis
		double I_yy;	//Moments of inertai about the rocket's pitch axis
		double I_zz;	//Moments of inertai about the rocket's roll axis

		//Reference inertia tensor

		double inertiaTensor[] = {{I_xx, 0, 0}, {0, I_yy, 0}, {0, 0, I_zz}};

	//Quaternion derivative
		double s_dot = 0.50 * dot(angVelocity, velocity);	//"dot" will be a dot product function, angular velocity has not been defined yet
		double v_dot = 0.50 * (s * angVelocity + cross(angVelocity, velocity))		//"cross" will be a cross product function
