using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using UnityEngine;

public class StandardMotor : Device
{
    private static Int16 DEVICE_ID = 0;
    private string _positiveDirection;
    private Int16[] _gears;
    private Int16 _resetAngle;
    private Int16 _speed;
    private Int16 _angle;
    private string _load;
    private Vector3 _rotationAxis;
    public GameObject attachedObject;
    public bool rotate_x;
    public bool rotate_y;
    public bool rotate_z;




    protected override void Start()
    {
        this.deviceID = DEVICE_ID;
        this.message_dict.Add(1, Info);
        this.message_dict.Add(2, Stop);
        this.message_dict.Add(3, Brake);
        this.message_dict.Add(4, Hold);
        this.message_dict.Add(5, Run);
        this.message_dict.Add(6, RunTime);
        this.message_dict.Add(7, RunAngle);
        this.message_dict.Add(8, RunTarget);
        this.message_dict.Add(9, TrackTarget);
        this.message_dict.Add(10, Angle);
        if (rotate_x) { _rotationAxis = Vector3.right; }
        if (rotate_y) { _rotationAxis = Vector3.up; }
        if (rotate_z) { _rotationAxis = Vector3.forward; }
        Debug.Log("ROTATION VECTOR : " + _rotationAxis.ToString());
        
        base.Start();
    }


    private string Info(string message_string)
    {
        Debug.Log("Info Message");
        InfoMessage message = JsonUtility.FromJson<InfoMessage>(message_string);
        // Implement Info Message
        _positiveDirection = message.positive_direction;
        if (_positiveDirection == "counter_clockwise") { _rotationAxis *= -1; }
        _gears = message.gears;
        _resetAngle = message.reset_angle;
        _speed = message.speed;
        _angle = message.angle;
        _load = message.load;
        Debug.Log(message_string);
        return JsonUtility.ToJson(new InfoReturnMessage());
        



    }

    private float GetCurrentRotationAngle() 
    {
        if (rotate_x)
        {
            return attachedObject.transform.localRotation.eulerAngles.x;
        }
        else if (rotate_y)
        {
            return attachedObject.transform.localRotation.eulerAngles.y;
        }
        else if (rotate_z)
        {
            return attachedObject.transform.localRotation.eulerAngles.z;
        }
        else
        {
            throw new Exception("None of the angle boxes were ticked");
        }
    }

    private string Angle(string message_string)
    {
        float angle = GetCurrentRotationAngle();
        Debug.Log("ANGLE : " + angle);
        AngleReturnMessage returnMessage = new AngleReturnMessage();
        returnMessage.angle = (int) angle;
        return JsonUtility.ToJson(returnMessage);
    }


    private string Stop(string message_string)
    {
        Debug.Log("Motor Stop");
        //Implement stop

        return JsonUtility.ToJson(new StopReturnMessage());
    }
    private string Brake(string message_string)
    {
        Debug.Log("Motor Brake");
        //Implement Brake

        return JsonUtility.ToJson(new BrakeReturnMessage());
    }

    private string Hold(string message_string)
    {
        Debug.Log("Motor Hold");
        //Implement Brake

        return JsonUtility.ToJson(new HoldReturnMessage());
    }
    private string Run(string message_string)
    {
        Debug.Log("Motor Run");
        //Implement Hold
        Debug.Log(message_string);
        RunMessage message = JsonUtility.FromJson<RunMessage>(message_string);
        return JsonUtility.ToJson(new RunReturnMessage());
    }

    private string RunTime(string message_string)
    {
        Debug.Log("Motor Run Time");
        //Implement Hold
        RunTimeMessage message = JsonUtility.FromJson<RunTimeMessage>(message_string);

        return JsonUtility.ToJson(new RunTimeReturnMessage());
    }

    private string RunAngle(string message_string)
    {
        Debug.Log("Motor Run Angle");
        RunAngleMessage message = JsonUtility.FromJson<RunAngleMessage>(message_string);
        return JsonUtility.ToJson(new RunAngleMessage());

    }

    private string RunTarget(string message_string)
    {
        Debug.Log("Motor Run Target");
        RunTargetMessage message = JsonUtility.FromJson<RunTargetMessage>(message_string);
        StartCoroutine(RotateSmoothly(targetAngle : message.target_angle,
                                      degreesPerSecond : message.speed));
        return JsonUtility.ToJson(new RunTargetMessage());
    }

    private string TrackTarget(string message_string)
    {
        Debug.Log("Motor Track Target");
        TrackTargetMessage message = JsonUtility.FromJson<TrackTargetMessage>(message_string);
        attachedObject.transform.localRotation = Quaternion.Euler(_rotationAxis * message.target_angle);
        return JsonUtility.ToJson(new TrackTargetMessage());
    }

    private class RunMessage
    {
        public int speed;
    }

    private class RunTimeMessage
    {
        public int speed;
        public int time;
        public bool wait;
        public string then;

    }

    private class RunAngleMessage
    {
        public int speed;
        public int rotation_angle;
        public bool wait;
        public string then;
    }

    private class RunTargetMessage
    {
        public int speed;
        public int target_angle;
        public bool wait;
        public string then;
    }

    private class TrackTargetMessage
    {
        public int target_angle;
    }


    private class InfoMessage
    {
        public string positive_direction;
        public Int16[] gears;
        public Int16 reset_angle;
        public Int16 speed;
        public Int16 angle;
        public string load;

    }

    private class InfoReturnMessage { }

    private class StopReturnMessage { }

    private class BrakeReturnMessage { }

    private class HoldReturnMessage { }

    private class RunReturnMessage { }

    private class RunTimeReturnMessage { }

    private class RunAngleReturnMessage { }

    private class RunTargetReturnMessage { }

    private class TrackTargetReturnMessage { }

    private class AngleReturnMessage 
    {
        public int angle;
    }



    IEnumerator RotateSmoothly(int targetAngle, int degreesPerSecond)
    {
        Quaternion desired_angle = Quaternion.Euler(_rotationAxis * targetAngle);
        while (true) {
            attachedObject.transform.Rotate(_rotationAxis * degreesPerSecond * Time.deltaTime);
            if (Quaternion.Angle(attachedObject.transform.localRotation, desired_angle) <= 0.1) 
            {
                attachedObject.transform.localRotation = desired_angle;
                Debug.Log("Hit required angle");
                break;
            }
            yield return new WaitForSeconds(0.0001f);
            Debug.Log("Not hit angle. Difference is : " + Quaternion.Angle(attachedObject.transform.localRotation, desired_angle));

        }
        yield return null;
    }


}
