using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UltrasonicSensor : Device
{
    private static Int16 DEVICE_ID = 1;

    protected override void Start()
    {
        this.deviceID = DEVICE_ID;
        //TODO : Move this into the device, make info an overridable method 
        this.message_dict.Add(1, Info);
        this.message_dict.Add(2, Distance);
        this.message_dict.Add(3, Presence);
        base.Start();
    }


    private string Info(string message_string)
    {
        Debug.Log("US Sensor Info Message");
        InfoMessage message = JsonUtility.FromJson<InfoMessage>(message_string);
        return JsonUtility.ToJson(new InfoReturnMessage());

    }

    private string Distance(string message_string) 
    {
        Debug.Log("US Sensor Distance");
        DistanceMessage message = JsonUtility.FromJson<DistanceMessage>(message_string);
        return JsonUtility.ToJson(new DistanceReturnMessage());
    }
    private string Presence(string message_string)
    {
        Debug.Log("US Sensor Presence");
        PresenceMessage message = JsonUtility.FromJson<PresenceMessage>(message_string);
        return JsonUtility.ToJson(new PresenceReturnMessage());
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
