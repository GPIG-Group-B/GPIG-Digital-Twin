using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Vehicle : MonoBehaviour
{

    public List<Wheel> wheels;

    public List<Wheel> drivingWheels;
    // Start is called before the first frame update
    private bool stoppingFlag = false;
    void Start()
    {
        foreach (Wheel eachWheel in wheels)
        {
            eachWheel.wheelCollider.ConfigureVehicleSubsteps(5.0f, 25, 5);
        }

    }

    // Update is called once per frame
    void Update()
    {
        foreach (Wheel eachWheel in wheels) 
        {
            UpdateWheelMeshTransform(wheelCollider: eachWheel.wheelCollider, wheelTransform: eachWheel.transform);
        }


    }

    void FixedUpdate()
    {
        foreach (Wheel eachWheel in drivingWheels)
        {
            if (!stoppingFlag & Mathf.Abs(eachWheel.wheelCollider.brakeTorque) > 0)
            {
                if (this.gameObject.GetComponent<Rigidbody>().velocity.magnitude > 0.000001f){
                    float max = 0.65f;
                    float min = 0.15f;
                    float velocity_scalar = (UnityEngine.Random.value * (max-min)) + min;
                    Debug.Log("Velocity scalar" + velocity_scalar);
                    this.gameObject.GetComponent<Rigidbody>().velocity *= velocity_scalar;
                    stoppingFlag = true;
                    Debug.Log("Setting flag");
                    break;
                }
            }
            else if (stoppingFlag & Mathf.Abs(eachWheel.wheelCollider.motorTorque) > 0)
            {
                Debug.Log("Resetting flag");
                stoppingFlag = false;
                break;
            }
            
        }

    }

    private void UpdateWheelMeshTransform(WheelCollider wheelCollider, Transform wheelTransform)
    {

        Vector3 position;
        Quaternion rotation;
        wheelCollider.GetWorldPose(out position, out rotation);


        wheelTransform.position = position;
        wheelTransform.rotation = rotation;
    }

    [Serializable]
    public class Wheel
    {
        public Transform transform;
        public WheelCollider wheelCollider;
    }
}
