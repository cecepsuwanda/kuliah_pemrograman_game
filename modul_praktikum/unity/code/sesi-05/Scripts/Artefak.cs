// Artefak.cs - trigger yang menambah skor dan memanggil bunyi pengambilan.
// Tempelkan pada artefak yang collider-nya bertanda Is Trigger.

using UnityEngine;

public class Artefak : MonoBehaviour
{
    public int nilai = 1;
    public string playerTag = "Player";
    public TampilanHud hud;
    public PemicuBunyi pemicuBunyi;

    [Header("Partikel (opsional)")]
    public ParticleSystem partikelAmbil;

    // Jumlah artefak yang telah diambil, dibaca oleh Pintu.
    public static int JumlahTerambil = 0;
    private bool sudahDiambil;

    void OnTriggerEnter2D(Collider2D other)
    {
        if (sudahDiambil || !other.CompareTag(playerTag)) return;

        sudahDiambil = true;
        JumlahTerambil += 1;

        // Bunyi dan partikel dipanggil pada peristiwa yang sama.
        if (pemicuBunyi != null) pemicuBunyi.Ambil();
        if (partikelAmbil != null) partikelAmbil.Play();

        if (hud != null) hud.TambahSkor(nilai);
        else Debug.LogWarning("Rujukan HUD pada artefak belum dihubungkan.");

        Debug.Log($"Artefak diambil. Total {JumlahTerambil} artefak.");
        gameObject.SetActive(false);
    }
}
