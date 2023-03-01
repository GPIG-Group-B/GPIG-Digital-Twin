using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Motor : Devices
{

    public Motor(string ip, int port)
    {
        init_device(ip, port, 0);

    }



}
