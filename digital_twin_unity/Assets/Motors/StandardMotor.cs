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

    private static UInt16 _INFO_MESSAGE_ID = 1;
    private static UInt16 _STOP_MESSAGE_ID = 2;
    private static UInt16 _BRAKE_MESSAGE_ID = 3;
    private static UInt16 _HOLD_MESSAGE_ID = 4;
    private static UInt16 _RUN_MESSAGE_ID = 5;
    private static UInt16 _RUN_TIME_MESSAGE_ID = 6;
    private static UInt16 _RUN_ANGLE_MESSAGE_ID = 7;
    private static UInt16 _RUN_TARGET_MESSAGE_ID = 8;
    private static UInt16 _TRACK_TARGET_MESSAGE_ID = 9;
    private static UInt16 _ANGLE_MESSAGE_ID = 10;




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
        this.message_dict.Add(_ANGLE_MESSAGE_ID, Angle);
        if (rotate_x) { _rotationAxis = Vector3.right; }
        if (rotate_y) { _rotationAxis = Vector3.up; }
        if (rotate_z) { _rotationAxis = Vector3.forward; }
        
        base.Start();
    }


    private void Info(string message_string)
    {
        Debug.Log("Info Message");
        InfoMessage message = JsonUtility.FromJson<InfoMessage>(message_string);
        // Implement Info Message
        _positiveDirection = message.positive_direction;
        if (_positiveDirection == "COUNTERCLOCKWISE") { _rotationAxis *= -1; }
        _gears = message.gears;
        _resetAngle = message.reset_angle;
        _speed = message.speed;
        _angle = message.angle;
        _load = message.load;
        Debug.Log(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new InfoReturnMessage()),
                                        messageID : _INFO_MESSAGE_ID);
        
        



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

    private void Angle(string message_string)
    {
        float angle = GetCurrentRotationAngle();
        AngleReturnMessage returnMessage = new AngleReturnMessage();
        returnMessage.angle = (int) angle;
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(returnMessage),
                                        messageID: _ANGLE_MESSAGE_ID);
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
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new RunReturnMessage()), _RUN_MESSAGE_ID);
    }

    private void RunTime(string message_string)
    {
        Debug.Log("Motor Run Time");
        //Implement Hold
        RunTimeMessage message = JsonUtility.FromJson<RunTimeMessage>(message_string);

        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new RunTimeReturnMessage()), _RUN_TIME_MESSAGE_ID);
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

        if (message.wait) 
        {

            StartCoroutine(RotateSmoothly(targetAngle: message.target_angle,
                                          degreesPerSecond: message.speed,
                                          messageID: _RUN_TARGET_MESSAGE_ID,
                                          message: JsonUtility.ToJson(new RunTargetMessage()))); 
        }
        else
        {
            StartCoroutine(RotateSmoothly(targetAngle: message.target_angle,
                              degreesPerSecond: message.speed));

            AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new RunTargetMessage()), _RUN_TARGET_MESSAGE_ID);
        }
    }

    private void TrackTarget(string message_string)
    {
        Debug.Log("Motor Track Target");
        TrackTargetMessage message = JsonUtility.FromJson<TrackTargetMessage>(message_string);
        attachedObject.transform.localRotation = Quaternion.Euler(_rotationAxis * message.target_angle);
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

    private class AngleReturnMessage 
    {
        public int angle;
    }



    IEnumerator RotateSmoothly(int targetAngle, int degreesPerSecond)
    {
        int directionFactor;
        float alpha = targetAngle - GetCurrentRotationAngle();
        float beta = alpha + 360;
        float gamma = alpha - 360;
        float[] possibleValues = { alpha, beta, gamma };
        float currentMinAbsValue = Mathf.Abs(possibleValues[0]);
        float currentShortestValue = possibleValues[0];
        for (int i = 1; i < 3; i++)
        {
            float absVal = Mathf.Abs(possibleValues[i]);
            if (absVal < currentMinAbsValue)
            {
                currentMinAbsValue = absVal;
                currentShortestValue = possibleValues[i];
            }
        }


        if (currentShortestValue < 0) { directionFactor = -1; }
        else { directionFactor = 1; }
        Quaternion desired_angle = Quaternion.Euler(_rotationAxis * targetAngle);
        while (true) {
            float angleDiff = Quaternion.Angle(attachedObject.transform.localRotation, desired_angle);
            if ( angleDiff <= 1) 
            {
                attachedObject.transform.localRotation = desired_angle;

                yield break;
            }

            attachedObject.transform.Rotate(_rotationAxis * degreesPerSecond * Time.deltaTime * directionFactor);
            yield return null;

        }
    }

    // TODO: Make this method less wasteful 
    IEnumerator RotateSmoothly(int targetAngle, int degreesPerSecond, UInt16 messageID, string message)
    {
        int directionFactor;
        float alpha = targetAngle - GetCurrentRotationAngle();
        float beta = alpha + 360;
        float gamma = alpha - 360;
        float[] possibleValues = { alpha, beta, gamma };
        float currentMinAbsValue = Mathf.Abs(possibleValues[0]);
        float currentShortestValue = possibleValues[0];
        for (int i = 1; i < 3; i++) 
        {
            float absVal = Mathf.Abs(possibleValues[i]);
            if (absVal < currentMinAbsValue) 
            {
                currentMinAbsValue = absVal;
                currentShortestValue = possibleValues[i];
            }
        }



        if (currentShortestValue < 0) { directionFactor = -1; }
        else { directionFactor = 1; }
        Debug.Log("DIRECTION FACTOR : " + directionFactor);
        Quaternion desired_angle = Quaternion.Euler(_rotationAxis * targetAngle);
        while (true)
        {
            if (Quaternion.Angle(attachedObject.transform.localRotation, desired_angle) <= 1)
            {
                attachedObject.transform.localRotation = desired_angle;
                AddReturnMessageToOutboundQueue(message, messageID);
                yield break;
            }
            attachedObject.transform.Rotate(_rotationAxis * degreesPerSecond * Time.deltaTime * directionFactor);
            yield return null;

        }


    }


}
