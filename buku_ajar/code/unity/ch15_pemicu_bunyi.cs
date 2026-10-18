// ch15_pemicu_bunyi.cs
// Menghubungkan peristiwa permainan dengan bunyinya.

using UnityEngine;

public class PemicuBunyi : MonoBehaviour
{
    public ManajerBunyi manajer;
    public TampilanHud hud;   // dari Bab XIV

    public int nilaiAmbil = 10;

    // Dipanggil oleh KontrolPemain ketika tombol lompat ditekan.
    public void Lompat()
    {
        if (manajer != null) manajer.BunyiLompat();
    }

    // Dipanggil ketika pemain menyentuh benda yang dapat diambil.
    void OnTriggerEnter2D(Collider2D lain)
    {
        if (!lain.CompareTag("Pickup")) return;

        if (manajer != null) manajer.BunyiAmbil();
        if (hud != null) hud.TambahSkor(nilaiAmbil);

        // Bendanya dimatikan supaya sentuhan yang sama tidak terhitung
        // dan berbunyi untuk kedua kalinya.
        lain.gameObject.SetActive(false);
    }

    public void Terluka(int jumlah)
    {
        if (manajer != null) manajer.BunyiTerluka();
        if (hud != null) hud.KurangiNyawa(jumlah);
    }

    public void Kalah()
    {
        if (manajer != null) manajer.BunyiKalah();
    }
}
