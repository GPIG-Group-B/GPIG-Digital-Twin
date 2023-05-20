using System.Collections;
using System.Collections.Generic;
using UnityEngine;




public class Output_logs : MonoBehaviour
{

    [SerializeField]
    public GameObject rover;

    [SerializeField]
    public Rigidbody roverRigidBody;

    public float distanceTravelled = 0;

    public List<SteeringMotor> steeringMotors;
    public List<UltrasonicSensor> us_sensors;

    public List<WheelMotor> wheelMotors;

    public List<ColourDistanceSensor> colourDistanceSensors;

    public List<ColourSensor> colourSensors;


    private bool showSidebar = false;

    private GUIStyle regularStyle;
    private GUIStyle colourSensorColour;

    private Color rgbTextColour;


    private Vector3 lastTrackedPosition;

    void Start()
    {
        regularStyle = new GUIStyle();
        regularStyle.normal = new GUIStyleState();
        regularStyle.normal.textColor = Color.white;
        regularStyle.normal.background = Texture2D.grayTexture;

        colourSensorColour = new GUIStyle();
        colourSensorColour.normal = new GUIStyleState();
        colourSensorColour.normal.textColor = Color.white;


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
            
            GUILayout.BeginArea(new Rect(10, 80, 300, 250),regularStyle);
            
            // display label for each wheel motor
            foreach (WheelMotor wm in wheelMotors)
            {
                
                Vector3 position;
                Quaternion rotation;
                wm.wheelCollider.GetWorldPose(out position, out rotation);
                float rpm =wm.wheelCollider.rpm;
                //output to gui the position and rotation of each wheel
                GUILayout.Label("Wheel " + wm.name + " position (x,y,z): " + position.ToString("0.00"));
                GUILayout.Label("Wheel " + wm.name + " rpm: " + rpm.ToString("0.00"));

            }

            foreach( ColourDistanceSensor cds in colourDistanceSensors){
                float h_ = cds.GetCurrentH();
                float s_ = cds.GetCurrentS();
                float v_ = cds.GetCurrentV();
                if ((h_ == 0f) & (s_ == 0f) & (v_ == 0f)){
                    rgbTextColour =Color.white;
                    GUILayout.Label("Colour Distance Sensor current view: No Colour detected.");
                }else{

                    rgbTextColour =Color.HSVToRGB(h_, s_, v_);
                    GUILayout.Label("Colour Distance Sensor HSV current view:");
                    colourSensorColour.normal.textColor = rgbTextColour;
                    GUILayout.Label("▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇",colourSensorColour);

                }
                
            }
            foreach(ColourSensor cs in colourSensors){
                float h_ = cs.GetCurrentH();
                float s_ = cs.GetCurrentS();
                float v_ = cs.GetCurrentV();
                if ((h_ == 0f) & (s_ == 0f) & (v_ == 0f)){
                    rgbTextColour =Color.white;
                    GUILayout.Label("Colour Sensor HSV current view: No Colour detected.");
                }else{

                    rgbTextColour =Color.HSVToRGB(h_, s_, v_);
                    GUILayout.Label("Colour Sensor current view:");
                    colourSensorColour.normal.textColor = rgbTextColour;
                    GUILayout.Label("▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇",colourSensorColour);
                }
            }


            GUILayout.EndArea();            
        }


        
        //display time taken and distance travelled at bottom of the screen
        //change this to a permanent box at the bottom

        GUI.Label(new Rect(10, Screen.height - 60, 300, 20), "Time elapsed : " + Time.time.ToString("0.00") + " seconds.",regularStyle );

        GUI.Label(new Rect(10, Screen.height - 40, 300, 20), "Distance travelled : " + distanceTravelled.ToString("0.00") + " meters.",regularStyle);
        GUI.Label(new Rect(10, Screen.height - 20, 300, 10), "Current speed: " + (roverRigidBody.velocity.magnitude/10).ToString("0.0000") + " m/s.",regularStyle);


    }
    


}
