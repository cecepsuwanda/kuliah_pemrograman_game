// ch13_trigger_pintu.cs
// Trigger volume: menandai bahwa pemain telah mencapai suatu tempat.

using UnityEngine;
using UnityEngine.Events;

public class TriggerPintu : MonoBehaviour
{
    public string playerTag = "Player";
    public UnityEvent onEnter;
    public UnityEvent onExit;

    private bool alreadyTriggered;

    // Dipanggil mesin ketika ada benda lain masuk ke dalam daerah trigger.
    // Metode ini hanya bekerja apabila collider benda ini ditandai sebagai
    // trigger, yaitu Is Trigger dicentang pada Inspector.
    void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag))
        {
            return;
        }

        if (alreadyTriggered)
        {
            return;
        }
        alreadyTriggered = true;

        Debug.Log($"Pemain masuk ke daerah {name} pada {Time.time:F1} detik.");
        onEnter.Invoke();
    }

    void OnTriggerExit2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag))
        {
            return;
        }

        Debug.Log($"Pemain keluar dari daerah {name}.");
        alreadyTriggered = false;
        onExit.Invoke();
    }
}
