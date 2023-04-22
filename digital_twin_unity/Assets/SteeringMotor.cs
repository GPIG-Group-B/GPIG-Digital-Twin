using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SteeringMotor : Device
{
    private static Int16 DEVICE_ID = 0;
    private string _positiveDirection;
    private Int16[] _gears;
    private Int16 _resetAngle;
    private Int16 _speed;
    private Int16 _angle;
    private string _load;

    public WheelCollider rightWheelCollider;
    public WheelCollider leftWheelCollider;


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
        base.Start();
    }


    private string Info(string message_string)
    {
        Debug.Log("Info Message");
        InfoMessage message = JsonUtility.FromJson<InfoMessage>(message_string);
        // Implement Info Message
        _positiveDirection = message.positive_direction;
        _gears = message.gears;
        _resetAngle = message.reset_angle;
        _speed = message.speed;
        _angle = message.angle;
        _load = message.load;
        Debug.Log(message_string);
        return JsonUtility.ToJson(new InfoReturnMessage());




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
        return JsonUtility.ToJson(new RunTargetMessage());
    }

    private string TrackTarget(string message_string)
    {
        Debug.Log("Motor Track Target");
        TrackTargetMessage message = JsonUtility.FromJson<TrackTargetMessage>(message_string);
        leftWheelCollider.steerAngle = message.target_angle;
        rightWheelCollider.steerAngle = message.target_angle;
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






}
