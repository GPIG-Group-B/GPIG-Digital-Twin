using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System;
using System.Linq;

public abstract class Devices
{ 

    private SocketHandler Socket;


    protected int port;
    protected int device_id;
    protected string ip;



    public void init_device(string ip,int port,int device_id)
    {
        this.ip = ip;
        this.port = port;
        this.device_id = device_id;
        this.Socket = new SocketHandler(ip: this.ip, port: this.port);
        Int16 received_device_id = this.Socket.setupSocket();
        // check right device id
        if (received_device_id != device_id)
        {
            throw new Exception("receive device id: "+ received_device_id + ". Expected device_id:" + device_id);

        }
        else
        {
            Debug.Log("recieved device id: " + received_device_id);
        }
    }

    public void run()
    {

        while (true)
        {
            var device_message_data =Socket.get_device_message();

            /*
            this.get_command(device_message_data.message_id);
            this.command(device_message_data.device_message);
            */



        }


    }



    


}
