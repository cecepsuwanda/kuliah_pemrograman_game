// PemicuBunyi.cs - penghubung peristiwa permainan dengan bunyinya.
// Tempelkan pada "Pemain", lalu hubungkan Manajer pada Inspector.

using UnityEngine;

public class PemicuBunyi : MonoBehaviour
{
    public ManajerBunyi manajer;

    // Dipanggil oleh KontrolPemain ketika tombol lompat ditekan.
    public void Lompat()
    {
        if (manajer != null) manajer.BunyiLompat();
    }

    // Dipanggil oleh Artefak ketika artefak tersentuh.
    public void Ambil()
    {
        if (manajer != null) manajer.BunyiAmbil();
    }

    // Dipanggil oleh TampilanHud ketika nyawa habis.
    public void Kalah()
    {
        if (manajer != null) manajer.BunyiKalah();
    }

    // Uji cepat tanpa harus kehabisan nyawa.
    [ContextMenu("Uji bunyi kalah")]
    void UjiKalah() { Kalah(); }
}
