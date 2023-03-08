using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System;
using System.Linq;

public class SocketHandler
{


    private string ip;// IP address to connect socket 

    private int port; // port to connect socket 

    private static int HEADER_SIZE = 2;


    private Socket socket;
    private byte[] encodedAcknowledgementMessage =  System.Text.Encoding.UTF8.GetBytes("GPIG-Group-B-Server");
    private byte[] encodedConnectionInitMessage = System.Text.Encoding.UTF8.GetBytes("GPIG-Group-B-Client");

    public SocketHandler(string ip, int port)
    {
        this.ip = ip;
        this.port = port;
        SetupSocket();
    }


    //function for sending data
    public void Send(byte[] Data_to_send)
    {
        socket.Send(Data_to_send);
    }

    //function for receiving data, takes length of data to receive as parameter, returns the bytes received as byte[]
    public byte[] ReceiveData(int lengthOfDataToReceive)
    {

        int numBytesReceived = 0;
        //allocate and receive bytes
        byte[] bytesReceived = new byte[lengthOfDataToReceive];

        while (numBytesReceived < lengthOfDataToReceive) {
            numBytesReceived += socket.Receive(buffer: bytesReceived, offset: numBytesReceived, socketFlags: SocketFlags.None, size: lengthOfDataToReceive - numBytesReceived) ;
            if (numBytesReceived == 0)
            {
                Debug.Log("NO BYTES received. CONNECTION CLOSED.");
            }
        }
        

        Debug.Log("The number of bytes received is: " +numBytesReceived);

        Debug.Log("The bytes converted to a string is: " + BitConverter.ToString(bytesReceived));

        

        return bytesReceived;
    }


    //sets up socket connection
    //connects to ip,port
    //sends connection init message
    //checks Acknowledgement message is correct
    public void SetupSocket()
    {

        //set up the new socket
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        //attempt to connect to the port
        try 
        {
            socket.Connect(ip, port); 
        }
        catch (SocketException e)
        { 
            Debug.LogException(e);
            Debug.Log(String.Format("Error connecting to IP : {0} | PORT : {1}. Waiting 3 seconds then retying",
                this.ip, this.port));
            System.Threading.Thread.Sleep(3000);
        }

        //send initialisation code
        Send(encodedConnectionInitMessage);

        //received bytes
        byte[] received_acknowledgement_message = ReceiveData(encodedAcknowledgementMessage.Length);

    }


    public (Int16, string) get_device_message()
    {
        Int16 messageID = GetHeaderData();
        Int16 messageSize = GetHeaderData();

        String message_json_string = System.Text.Encoding.UTF8.GetString(ReceiveData(lengthOfDataToReceive: messageSize));


        return (messageID, message_json_string);
    }

    public Int16 GetHeaderData() 
    {
        return BitConverter.ToInt16(ReceiveData(lengthOfDataToReceive: HEADER_SIZE), 0);
    }



    //helper function to close connection
    public void closeConnection()
    {
        socket.Close();
    }



}
