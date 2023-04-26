using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UltrasonicSensor : Device
{
    private static Int16 DEVICE_ID = 1;

    private static UInt16 _INFO_MESSAGE_ID = 1;
    private static UInt16 _DISTANCE_MESSAGE_ID = 2;
    private static UInt16 _PRESENCE_MESSAGE_ID = 3;

    protected override void Start()
    {
        this.deviceID = DEVICE_ID;
        //TODO : Move this into the device, make info an overridable method 
        this.message_dict.Add(_INFO_MESSAGE_ID, Info);
        this.message_dict.Add(_DISTANCE_MESSAGE_ID, Distance);
        this.message_dict.Add(_PRESENCE_MESSAGE_ID, Presence);
        base.Start();
    }


    private void Info(string message_string)
    {
        Debug.Log("US Sensor Info Message");
        InfoMessage message = JsonUtility.FromJson<InfoMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new InfoReturnMessage()), _INFO_MESSAGE_ID);

    }

    private void Distance(string message_string) 
    {
        Debug.Log("US Sensor Distance");
        DistanceMessage message = JsonUtility.FromJson<DistanceMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new DistanceReturnMessage()), _DISTANCE_MESSAGE_ID);
    }
    private void Presence(string message_string)
    {
        Debug.Log("US Sensor Presence");
        PresenceMessage message = JsonUtility.FromJson<PresenceMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new PresenceReturnMessage()), _PRESENCE_MESSAGE_ID);
    }


    private class DistanceMessage
    {
    }

    private class PresenceMessage
    {
    }

    private class InfoMessage
    {
    }

    private class InfoReturnMessage { }
    private class DistanceReturnMessage 
    {
        public Int16 distance;
    }

    private class PresenceReturnMessage
    {
        public bool presence;
    }







}
