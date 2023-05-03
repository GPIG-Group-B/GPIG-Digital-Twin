using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class ColourDistanceSensor : Device
{
    private static Int16 DEVICE_ID = 2;

    private static UInt16 _INFO_MESSAGE_ID = 1;
    private static UInt16 _COLOUR_MESSAGE_ID = 2;
    private static UInt16 _REFLECTION_MESSAGE_ID = 3;
    private static UInt16 _AMBIENT_MESSAGE_ID = 4;
    private static UInt16 _DISTANCE_MESSAGE_ID = 5;

    protected override void Start()
    {
        this.deviceID = DEVICE_ID;
        //TODO : Move this into the device, make info an overridable method 
        this.message_dict.Add(_INFO_MESSAGE_ID, Info);
        this.message_dict.Add(_COLOUR_MESSAGE_ID, Colour);
        this.message_dict.Add(_REFLECTION_MESSAGE_ID, Reflection);
        this.message_dict.Add(_AMBIENT_MESSAGE_ID, Ambient);
        this.message_dict.Add(_DISTANCE_MESSAGE_ID, Distance);
        base.Start();
    }


    private void Info(string message_string)
    {
        Debug.Log("US Sensor Info Message");
        InfoMessage message = JsonUtility.FromJson<InfoMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new InfoReturnMessage()), _INFO_MESSAGE_ID);

    }

    private void Colour(string message_string)
    {
        Debug.Log("Colour Sensor Colour");
        ColourMessage message = JsonUtility.FromJson<ColourMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new ColourReturnMessage()), _COLOUR_MESSAGE_ID);
    }

    private void Reflection(string message_string)
    {
        Debug.Log("Colour Sensor reflection");
        ReflectionMessage message = JsonUtility.FromJson<ReflectionMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new ReflectionReturnMessage()), _REFLECTION_MESSAGE_ID);
    }

    private void Ambient(string message_string)
    {
        Debug.Log("Colour Sensor ambient");
        AmbientMessage message = JsonUtility.FromJson<AmbientMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new AmbientReturnMessage()), _AMBIENT_MESSAGE_ID);
    }

    private void Distance(string message_string)
    {
        Debug.Log("Colour Sensor reflection");
        DistanceMessage message = JsonUtility.FromJson<DistanceMessage>(message_string);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(new DistanceReturnMessage()), _DISTANCE_MESSAGE_ID);
    }

    private class DistanceMessage
    {
    }

    private class InfoMessage { }

    private class ColourMessage
    {
        public bool surface;
    }

    private class ReflectionMessage
    {
    }

    private class AmbientMessage
    {
    }

    private class InfoReturnMessage { }
    private class ColourReturnMessage
    {
        public Color colour;
    }

    private class ReflectionReturnMessage
    {
        public UInt16 reflection;
    }

    private class DistanceReturnMessage
    {
        public UInt16 distance;
    }

    private class AmbientReturnMessage
    {
        public UInt16 ambient_light;
    }







}
