using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class ForceSensor : Device
{
    private static Int16 DEVICE_ID = 3;

    private static UInt16 _INFO_MESSAGE_ID = 1;
    private static UInt16 _FORCE_MESSAGE_ID = 2;
    private static UInt16 _DISTANCE_MESSAGE_ID = 3;
    private static UInt16 _PRESSED_MESSAGE_ID = 4;
    private static UInt16 _TOUCHED_MESSAGE_ID = 5;

    private bool _is_touched;

    protected override void Start()
    {
        this.deviceID = DEVICE_ID;
        //TODO : Move this into the device, make info an overridable method 
        this.message_dict.Add(_INFO_MESSAGE_ID, Info);
        this.message_dict.Add(_FORCE_MESSAGE_ID, Force);
        this.message_dict.Add(_DISTANCE_MESSAGE_ID, Distance);
        this.message_dict.Add(_PRESSED_MESSAGE_ID, Pressed);
        this.message_dict.Add(_TOUCHED_MESSAGE_ID, Touched);
        base.Start();
    }

    private void OnTriggerEnter(Collider other)
    {
        _is_touched = true;
    }
    private void OnTriggerExit(Collider other)
    {
        _is_touched = false;
    }



    private void Info(string message_string)
    {
        Debug.Log("US Sensor Info Message");
        InfoMessage message = JsonUtility.FromJson<InfoMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new InfoReturnMessage()), _INFO_MESSAGE_ID);

    }

    private void Force(string message_string)
    {
        Debug.Log("Force Sensor Force");
        ForceMessage message = JsonUtility.FromJson<ForceMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new ForceReturnMessage()), _FORCE_MESSAGE_ID);
    }

    private void Distance(string message_string)
    {
        Debug.Log("Colour Sensor reflection");
        DistanceMessage message = JsonUtility.FromJson<DistanceMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new DistanceReturnMessage()), _DISTANCE_MESSAGE_ID);
    }

    private void Pressed(string message_string)
    {
        Debug.Log("Colour Sensor ambient");
        PressedMessage message = JsonUtility.FromJson<PressedMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new PressedReturnMessage()), _PRESSED_MESSAGE_ID);
    }

    private void Touched(string message_string)
    {
        Debug.Log("Colour Sensor ambient");
        TouchedMessage message = JsonUtility.FromJson<TouchedMessage>(message_string);
        TouchedReturnMessage returnMessage = new TouchedReturnMessage();
        returnMessage.is_touched = _is_touched;
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(returnMessage), _TOUCHED_MESSAGE_ID);
    }

    private class InfoMessage { }

    private class ForceMessage
    {
    }

    private class DistanceMessage
    {
    }

    private class PressedMessage
    {
    }

    private class TouchedMessage
    {
    }

    private class InfoReturnMessage { }
    private class ForceReturnMessage
    {
        public UInt16 force;
    }

    private class DistanceReturnMessage
    {
        public UInt16 distance;
    }

    private class PressedReturnMessage
    {
        public bool is_pressed;
    }

    private class TouchedReturnMessage
    {
        public bool is_touched;
    }

    public bool GetIsTouched()
    {
        return _is_touched;
    }






}
