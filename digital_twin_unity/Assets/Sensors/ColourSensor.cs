using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEditor.UI;
using UnityEngine;

public class ColourSensor : Device
{
    private static Int16 DEVICE_ID = 2;

    private static UInt16 _INFO_MESSAGE_ID = 1;
    private static UInt16 _COLOUR_MESSAGE_ID = 2;
    private static UInt16 _REFLECTION_MESSAGE_ID = 3;
    private static UInt16 _AMBIENT_MESSAGE_ID = 4;
    private float _h;
    private float _s;
    private float _v;

    protected override void Start()
    {
        this.deviceID = DEVICE_ID;
        //TODO : Move this into the device, make info an overridable method 
        this.message_dict.Add(_INFO_MESSAGE_ID, Info);
        this.message_dict.Add(_COLOUR_MESSAGE_ID, Colour);
        this.message_dict.Add(_REFLECTION_MESSAGE_ID, Reflection);
        this.message_dict.Add(_AMBIENT_MESSAGE_ID , Ambient);
        base.Start();
    }

    void FixedUpdate() 
    {



        Color colourReceived;
        RaycastHit hit;
        Vector3 fwd = transform.TransformDirection(transform.up);
        // 0.5 as max distance is 5cm. Everything is scaled by 10
        Debug.DrawRay(transform.position, fwd * 0.6f, Color.green);
        if (Physics.Raycast(transform.position, fwd, out hit, 0.6f))
        {
            Renderer renderer = hit.collider.gameObject.GetComponent<Renderer>();
            colourReceived = renderer.material.color;
            Debug.Log("Color Sensor - Detected colour : " + colourReceived);
            // You can now use the hitColor variable to access the color of the hit object.
        }
        else
        {
            Debug.Log("Color Sensor - No colour detected");
            colourReceived = new Color(r: -1.0f, g: -1.0f, b: -1.0f);
        }
        if (colourReceived.r == -1.0f)
        {
            _h = 0.0f;
            _s = 0.0f;
            _v = 0.0f;
        }
        else
        {
            Color.RGBToHSV(colourReceived, out _h, out _s, out _v);
        }
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
        ColourReturnMessage returnMessage = new ColourReturnMessage();
        returnMessage.h = _h * 360f;
        returnMessage.s = _s * 100f;
        returnMessage.v = _v * 100f;
        Debug.Log("Colour | H : " + returnMessage.h + " | S : " + returnMessage.s + " | V : " + returnMessage.v);
        AddReturnMessageToOutboundQueue(JsonUtility.ToJson(returnMessage), _COLOUR_MESSAGE_ID);
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
        public float h;
        public float s;
        public float v;
    }


    private class ReflectionReturnMessage
    {
        public UInt16 reflection;
    }

    private class AmbientReturnMessage
    {
        public UInt16 ambient_light;
    }

    public float GetCurrentH() 
    {
        return _h;
    }

    public float GetCurrentS()
    {
        return _s;
    }

    public float GetCurrentV()
    {
        return _v;
    }






}
