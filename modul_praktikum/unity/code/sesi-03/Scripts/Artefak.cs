// Artefak.cs - trigger yang menambah skor HUD ketika artefak diambil.
// Tempelkan pada artefak yang collider-nya bertanda Is Trigger.

using UnityEngine;

public class Artefak : MonoBehaviour
{
    public int nilai = 1;
    public string playerTag = "Player";
    public TampilanHud hud;

    // Jumlah artefak yang telah diambil, dibaca oleh Pintu.
    public static int JumlahTerambil = 0;
    private bool sudahDiambil;

    void OnTriggerEnter2D(Collider2D other)
    {
        if (sudahDiambil || !other.CompareTag(playerTag)) return;

        sudahDiambil = true;
        JumlahTerambil += 1;
        if (hud != null) hud.TambahSkor(nilai);
        else Debug.LogWarning("Rujukan HUD pada artefak belum dihubungkan.");

        Debug.Log($"Artefak diambil. Total {JumlahTerambil} artefak.");
        gameObject.SetActive(false);
    }
}
