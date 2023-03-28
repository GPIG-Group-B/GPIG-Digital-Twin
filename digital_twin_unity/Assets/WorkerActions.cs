using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEngine;

public class WorkerActions : MonoBehaviour
{
    public SocketHandler SocketControlScript;
    private byte[] MotorDeviceID= System.Text.Encoding.UTF8.GetBytes("0");
    /*private byte[] MotorDeviceID = System.Text.Encoding.UTF8.GetBytes("1");
    private byte[] MotorDeviceID = System.Text.Encoding.UTF8.GetBytes("2");
    private byte[] MotorDeviceID = System.Text.Encoding.UTF8.GetBytes("3");
    private byte[] MotorDeviceID = System.Text.Encoding.UTF8.GetBytes("4");
    private byte[] MotorDeviceID = System.Text.Encoding.UTF8.GetBytes("3");
    private byte[] MotorDeviceID = System.Text.Encoding.UTF8.GetBytes("4");*/



    // Start is called before the first frame update
    void Awake()
    {
        SocketControlScript = GetComponent<SocketHandler>();
        SocketControlScript.SetupSocket();
        SocketControlScript.closeConnection(); // for testing only
    }

    //From here we call the receive for all devices and perform action





    private void Start()
    {

    }

    // This function is called every fixed framerate frame, if the MonoBehaviour is enabled
    private void FixedUpdate()
    {
 


    }



    // Update is called once per frame
    void Update()
    {

      

    }
}
