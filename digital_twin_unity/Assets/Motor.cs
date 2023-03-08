using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Motor : Device
{
    private static Int16 DEVICE_ID = 0;



    public Motor(string ip, int port) : base(ip : ip , port : port, deviceID : DEVICE_ID)
    {
        this.message_dict.Add(1, Stop);
        this.message_dict.Add(2, Brake);
        this.message_dict.Add(3, Hold);
        this.message_dict.Add(4, Run);
        this.message_dict.Add(5, RunTime);

    }

    private static void Stop(string message_string)
    {
        Debug.Log("Motor Stop");
        //Implement stop
    }
    private static void Brake(string message_string)
    {
        Debug.Log("Motor Brake");
        //Implement Brake
    }

    private static void Hold(string message_string)
    {
        Debug.Log("Motor Hold");
        //Implement Brake
    }
    private static void Run(string message_string)
    {
        Debug.Log("Motor Run");
        //Implement Hold
        RunMessage message = JsonUtility.FromJson<RunMessage>(message_string);
    }

    private static void RunTime(string message_string)
    {
        Debug.Log("Motor Run");
        //Implement Hold
        RunTimeMessage message = JsonUtility.FromJson<RunTimeMessage>(message_string);
    }

    private class RunMessage 
    {
        public int speed { get; set; }
    }

    private class RunTimeMessage 
    {
        public int speed { get; set; }
        public int time { get; set; }
        public bool wait { get; set; }
        public string then { get; set; }

    }






}
