using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Vehicle : MonoBehaviour
{

    public List<Wheel> wheels;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        foreach (Wheel eachWheel in wheels) 
        {
            UpdateWheelMeshTransform(wheelCollider: eachWheel.wheelCollider, wheelTransform: eachWheel.transform);
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
