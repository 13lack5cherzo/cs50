using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class FloorDespawn : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (GameObject.Find("FPSController").transform.position.y < -1) {
            LevelGenerator.playerLevel = 0;  // reset score
            SceneManager.LoadScene("GameOver");  // go to gameover scene
        }
    }
}
