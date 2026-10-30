// Artefak.cs
// Trigger yang menandai sebuah artefak telah diambil.
// Tempelkan pada GameObject artefak yang collider-nya bertanda Is Trigger.

using UnityEngine;

public class Artefak : MonoBehaviour
{
    public int nilai = 1;
    public string playerTag = "Player";

    // Jumlah artefak yang telah diambil, dibaca oleh Pintu.
    public static int JumlahTerambil = 0;

    private bool sudahDiambil;

    void OnTriggerEnter2D(Collider2D other)
    {
        if (sudahDiambil)
        {
            return;
        }
        if (!other.CompareTag(playerTag))
        {
            return;
        }

        sudahDiambil = true;
        JumlahTerambil += 1;
        Debug.Log($"Artefak diambil. Total {JumlahTerambil} artefak.");

        // Artefak lenyap dari scene setelah diambil.
        gameObject.SetActive(false);
    }
}
