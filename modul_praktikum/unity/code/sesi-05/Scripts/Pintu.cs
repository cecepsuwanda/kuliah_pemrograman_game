// Pintu.cs
// Trigger yang memeriksa syarat artefak sebelum level dinyatakan selesai.
// Tempelkan pada GameObject pintu yang collider-nya bertanda Is Trigger.

using UnityEngine;

public class Pintu : MonoBehaviour
{
    public string playerTag = "Player";
    public int artefakDiperlukan = 3;

    private bool sudahTerbuka;

    void OnTriggerEnter2D(Collider2D other)
    {
        if (sudahTerbuka)
        {
            return;
        }
        if (!other.CompareTag(playerTag))
        {
            return;
        }

        if (Artefak.JumlahTerambil < artefakDiperlukan)
        {
            Debug.Log($"Pintu terkunci. Artefak {Artefak.JumlahTerambil} " +
                      $"dari {artefakDiperlukan}.");
            return;
        }

        sudahTerbuka = true;
        Debug.Log("Pintu terbuka. Level selesai.");
    }

    void OnTriggerExit2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag))
        {
            return;
        }
        Debug.Log("Pemain meninggalkan daerah pintu.");
    }
}
