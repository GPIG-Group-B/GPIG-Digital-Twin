using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;

public class Rover : MonoBehaviour
{
    Motor driving_motor;

    private void Start()
    {
        throw new NotImplementedException();


    }

    public static void sub_thread_device(Type deviceType) 
    {

        DeviceType instance = (DeviceType)Activator.CreateInstance(deviceType);
    }

}


