using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WheelMotor : Device
{
    private static Int16 DEVICE_ID = 0;
    private string _positiveDirection;
    private Int16[] _gears;
    private Int16 _resetAngle;
    private Int16 _speed;
    private Int16 _angle;
    private string _load;

    public WheelCollider wheelCollider;

    private static UInt16 _INFO_MESSAGE_ID = 1;
    private static UInt16 _STOP_MESSAGE_ID = 2;
    private static UInt16 _BRAKE_MESSAGE_ID = 3;
    private static UInt16 _HOLD_MESSAGE_ID = 4;
    private static UInt16 _RUN_MESSAGE_ID = 5;
    private static UInt16 _RUN_TIME_MESSAGE_ID = 6;
    private static UInt16 _RUN_ANGLE_MESSAGE_ID = 7;
    private static UInt16 _RUN_TARGET_MESSAGE_ID = 8;
    private static UInt16 _TRACK_TARGET_MESSAGE_ID = 9;





    protected override void Start()
    {
        this.deviceID = DEVICE_ID;
        this.message_dict.Add(_INFO_MESSAGE_ID, Info);
        this.message_dict.Add(_STOP_MESSAGE_ID, Stop);
        this.message_dict.Add(_BRAKE_MESSAGE_ID, Brake);
        this.message_dict.Add(_HOLD_MESSAGE_ID, Hold);
        this.message_dict.Add(_RUN_MESSAGE_ID, Run);
        this.message_dict.Add(_RUN_TIME_MESSAGE_ID, RunTime);
        this.message_dict.Add(_RUN_ANGLE_MESSAGE_ID, RunAngle);
        this.message_dict.Add(_RUN_TARGET_MESSAGE_ID, RunTarget);
        this.message_dict.Add(_TRACK_TARGET_MESSAGE_ID, TrackTarget);

        base.Start();
    }


    private void Info(string message_string)
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
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new InfoReturnMessage()), _INFO_MESSAGE_ID);




    }




    private void Stop(string message_string)
    {
        Debug.Log("Motor Stop");
        //Implement stop

        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new StopReturnMessage()), _STOP_MESSAGE_ID);
    }
    private void Brake(string message_string)
    {
        Debug.Log("Motor Brake");
        //Implement Brake

        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new BrakeReturnMessage()), _BRAKE_MESSAGE_ID);
    }

    private void Hold(string message_string)
    {
        Debug.Log("Motor Hold");
        //Implement Brake

        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new HoldReturnMessage()), _HOLD_MESSAGE_ID);
    }
    private void Run(string message_string)
    {
        Debug.Log("Motor Run");
        //Implement Hold
        Debug.Log(message_string);
        RunMessage message = JsonUtility.FromJson<RunMessage>(message_string);
        wheelCollider.motorTorque = message.speed;
        Debug.Log("Set motor speed to : " + message.speed);
        Debug.Log(wheelCollider.rpm);

        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new RunReturnMessage()), _RUN_MESSAGE_ID);
    }

    private void RunTime(string message_string)
    {
        Debug.Log("Motor Run Time");
        //Implement Hold
        string returnMessage = JsonUtility.ToJson(new RunTimeReturnMessage())
        RunTimeMessage message = JsonUtility.FromJson<RunTimeMessage>(message_string);
        if (message.wait)
        {
            StartCoroutine(ApplyTorqueTime(torque: message.speed,
                                           seconds: message.time,
                                           messageID : _RUN_TIME_MESSAGE_ID,
                                           message : returnMessage));
        }
        else 
        {
            StartCoroutine(ApplyTorqueTime(torque: message.speed, seconds: message.time));
            AddReturnMessageToOutboundQueue(returnMessage,
                                            _RUN_TIME_MESSAGE_ID);
        }
        
    }

    private void RunAngle(string message_string) 
    {
        Debug.Log("Motor Run Angle");
        RunAngleMessage message = JsonUtility.FromJson<RunAngleMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new RunAngleMessage()), _RUN_ANGLE_MESSAGE_ID);

    }

    private void RunTarget(string message_string) 
    {
        Debug.Log("Motor Run Target");
        RunTargetMessage message = JsonUtility.FromJson<RunTargetMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new RunTargetMessage()), _RUN_TARGET_MESSAGE_ID); 
    }

    private void TrackTarget(string message_string) 
    {
        Debug.Log("Motor Track Target");
        TrackTargetMessage message = JsonUtility.FromJson<TrackTargetMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new TrackTargetMessage()), _TRACK_TARGET_MESSAGE_ID);
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



    IEnumerator ApplyTorqueTime(int torque, int seconds)
    {
        wheelCollider.motorTorque = torque;
        bool completed = false;
        if (!completed)
        {
            completed = true;
            yield return new WaitForSeconds(seconds);

        }
        wheelCollider.motorTorque = 0;
        wheelCollider.brakeTorque = 100;
        yield return null;
    }

    IEnumerator ApplyTorqueTime(int torque, int seconds, UInt16 messageID, string message)
    {
        wheelCollider.motorTorque = torque;
        bool completed = false;
        if (!completed)
        {
            completed = true;
            yield return new WaitForSeconds(seconds);

        }
        wheelCollider.motorTorque = 0;
        wheelCollider.brakeTorque = 100;
        AddReturnMessageToOutboundQueue(message, messageID);
        yield return null;
    }



}
