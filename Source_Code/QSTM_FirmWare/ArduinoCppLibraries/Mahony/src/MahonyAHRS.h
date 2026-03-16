//=====================================================================================================
// MahonyAHRS.h
//=====================================================================================================
//
// Madgwick's implementation of Mayhony's AHRS algorithm.
// See: http://www.x-io.co.uk/open-source-imu-and-ahrs-algorithms/
//
// Date			Author			Notes
// 29/09/2011	SOH Madgwick    Initial release
// 02/10/2011	SOH Madgwick	Optimised for reduced CPU load
//
//=====================================================================================================
#ifndef MahonyAHRS_h
#define MahonyAHRS_h
#include <math.h>

//----------------------------------------------------------------------------------------------------
// Variable declaration

class Mahony {
private:
	float twoKp;		// 2 * proportional gain (Kp)
	float twoKi;		// 2 * integral gain (Ki)
	float q0, q1, q2, q3;	// quaternion of sensor frame relative to auxiliary frame
	float integralFBx, integralFBy, integralFBz;  // integral error terms scaled by Ki
	static float invSqrt(float x);
	float invSampleFreq;
	float roll;
    float pitch;
    float yaw;

//---------------------------------------------------------------------------------------------------
// Function declarations

public:
	Mahony();
	void begin(float sampleFrequency) { invSampleFreq = 1.0f / sampleFrequency; }
	void update(float gx, float gy, float gz, float ax, float ay, float az, float mx, float my, float mz);
	void updateIMU(float gx, float gy, float gz, float ax, float ay, float az);
	
	float getPitchRadians(){
		pitch = atan2f(2.0f * q2 * q3 - 2.0f * q0 * q1, 2.0f * q0 * q0 + 2.0f * q3 * q3 - 1.0f);
		return pitch; 
	};
	float getRollRadians(){
		roll = -1.0f * asinf(2.0f * q1 * q3 + 2.0f * q0 * q2);
		return roll;
	};
	float getYawRadians(){
		yaw = atan2f(2.0f * q1 * q2 - 2.0f * q0 * q3, 2.0f * q0 * q0 + 2.0f * q1 * q1 - 1.0f);
		return yaw;
	};
	float getRoll() {
        roll = getRollRadians();
        return roll * 57.29578f;
    }
    float getPitch() {
        pitch = getPitchRadians();
        return pitch * 57.29578f;
    }
    float getYaw() {
		yaw = getYawRadians();      
        return yaw * 57.29578f + 180.0f;
    }
	float getQnW(){return q0;}
	float getQnX(){return q1;}
	float getQnY(){return q2;}
	float getQnZ(){return q3;}
};

#endif
//=====================================================================================================
// End of file
//=====================================================================================================
