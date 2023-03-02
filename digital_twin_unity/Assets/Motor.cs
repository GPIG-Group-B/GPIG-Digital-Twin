using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Motor : Device
{
    private static int DEVICE_ID = 0;
    public Motor(string ip, int port) : base(ip : ip , port : port, device_id : DEVICE_ID)
    {

    }



}
