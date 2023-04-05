using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Motor : Device
{
    private static Int16 DEVICE_ID = 0;
    private string _positiveDirection;
    private Int16[] _gears;
    private Int16 _resetAngle;
    private Int16 _speed;
    private Int16 _angle;
    private string _load;

    public WheelCollider wheelCollider;


    protected override void Start() 
    {
        this.deviceID = DEVICE_ID;
        this.message_dict.Add(1, Info);
        this.message_dict.Add(2, Stop);
        this.message_dict.Add(3, Brake);
        this.message_dict.Add(4, Hold);
        this.message_dict.Add(5, Run);
        this.message_dict.Add(6, RunTime);
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
        wheelCollider.motorTorque = message.speed;
        Debug.Log("Set motor speed to : " + message.speed);
        Debug.Log(wheelCollider.rpm);

        return JsonUtility.ToJson(new RunReturnMessage());
    }

    private string RunTime(string message_string)
    {
        Debug.Log("Motor Run");
        //Implement Hold
        RunTimeMessage message = JsonUtility.FromJson<RunTimeMessage>(message_string);

        return JsonUtility.ToJson(new RunTimeReturnMessage());
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






}
