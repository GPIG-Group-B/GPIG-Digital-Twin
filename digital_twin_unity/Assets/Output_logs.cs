using System.Collections;
using System.Collections.Generic;
using UnityEngine;




public class Output_logs : MonoBehaviour
{

    [SerializeField]
    public GameObject rover;

    public float distanceTravelled = 0;

    public List<SteeringMotor> steeringMotors;
    public List<UltrasonicSensor> us_sensors;

    public List<WheelMotor> wheelMotors;

    public List<ColourDistanceSensor> colourDistanceSensors;

    public List<ColourSensor> colourSensors;


    private bool showSidebar = false;

    private GUIStyle style;



    private Vector3 lastTrackedPosition;

    void Start()
    {
        lastTrackedPosition = rover.transform.position;
    }

    void FixedUpdate()
    {
        Vector3 currentPosition = rover.transform.position;

        //To ignore vertical movement
        currentPosition.y = lastTrackedPosition.y;

        distanceTravelled += (Vector3.Distance(currentPosition, lastTrackedPosition))/10;

        lastTrackedPosition = currentPosition;

    }

    void OnGUI()
    {
        style = new GUIStyle();
        style.normal = new GUIStyleState();
        style.normal.textColor = Color.white;
        style.normal.background = Texture2D.grayTexture;
        ///debugging distance travelled

        //add a button that toggles a sidebar to display the current state of the car
        if (GUI.Button(new Rect(10, 10, 100, 50), "Toggle Sidebar"))
        {
            //toggle the sidebar
            showSidebar = !showSidebar;
        }
        if (showSidebar)
        {
            //display the sidebar
            //create rectangle for the sidebar
            
            GUILayout.BeginArea(new Rect(10, 80, 300, 250),style);
            
            // display label for each wheel motor
            foreach (WheelMotor wm in wheelMotors)
            {

                Vector3 position;
                Quaternion rotation;
                wm.wheelCollider.GetWorldPose(out position, out rotation);
                //output to gui the position and rotation of each wheel
                GUILayout.Label("Wheel " + wm.name + " position (x,y,z): " + position.ToString("0.00"));
                GUILayout.Label("Wheel " + wm.name + " rotation (x,y,z): " + rotation.eulerAngles.ToString("0.00"));

            }

            foreach( ColourDistanceSensor cds in colourDistanceSensors){
                GUILayout.Label("<There will be some colour distance sensor info here>");
            }
            foreach(ColourSensor cs in colourSensors){
                GUILayout.Label("<There will be some colour sensor info here>");
            }

            GUILayout.EndArea();            
        }


        
        //display time taken and distance travelled at bottom of the screen
        GUI.Label(new Rect(10, Screen.height - 50, 300, 20), "Time elapsed : " + Time.time.ToString("0.00") + " seconds.",style );

        GUI.Label(new Rect(10, Screen.height - 30, 300, 20), "Distance travelled : " + distanceTravelled.ToString("0.00") + " meters.",style);
        


    }
    


}
