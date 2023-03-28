using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using UnityEngine;

public class Rover : MonoBehaviour
{

    private void Start()
    {

        Motor motor1 = new Motor(ip: "localhost", port: 65432);

        // Create a thread to execute the task, and then
        // start the thread.
        Thread t = new Thread(new ThreadStart(motor1.run));
        t.Start();
        Console.WriteLine("Main thread does some work, then waits.");
        t.Join();
        Console.WriteLine("Independent task has completed; main thread ends.");
    }


}





