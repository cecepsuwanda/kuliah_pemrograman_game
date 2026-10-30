// TampilanHud.cs - menampilkan skor dan nyawa, serta memanggil bunyi kalah.
// Tempelkan pada "Canvas", lalu hubungkan rujukannya pada Inspector.

using UnityEngine;
using UnityEngine.UI;

public class TampilanHud : MonoBehaviour
{
    public Text scoreText;
    public Text livesText;
    public Image[] heartIcons;

    [Header("Bunyi")]
    public PemicuBunyi pemicuBunyi;

    private int score;
    private int lives = 3;

    void Start()
    {
        // Rujukan yang kosong adalah penyebab kesalahan yang paling sering.
        if (scoreText == null || livesText == null)
        {
            Debug.LogWarning("Rujukan teks belum dihubungkan pada Inspector.");
            enabled = false;
            return;
        }
        PerbaruiTampilan();
    }

    public void TambahSkor(int nilai)
    {
        score += nilai;
        PerbaruiTampilan();
        Debug.Log($"Skor sekarang {score}");
    }

    public void KurangiNyawa(int nilai)
    {
        lives = Mathf.Max(0, lives - nilai);
        PerbaruiTampilan();

        if (lives == 0)
        {
            Debug.Log("Nyawa habis.");
            if (pemicuBunyi != null) pemicuBunyi.Kalah();
        }
    }

    // Uji cepat dari menu konteks komponen ketika scene berjalan.
    [ContextMenu("Uji kurangi satu nyawa")]
    void UjiKurangiNyawa() { KurangiNyawa(1); }

    void PerbaruiTampilan()
    {
        scoreText.text = $"Skor: {score}";
        livesText.text = $"Nyawa: {lives}";
        for (int i = 0; i < heartIcons.Length; i++)
        {
            if (heartIcons[i] != null) heartIcons[i].enabled = i < lives;
        }
    }
}
