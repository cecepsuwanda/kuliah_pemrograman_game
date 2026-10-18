// ch14_tampilan_hud.cs
// Antarmuka pengguna: menampilkan skor dan nyawa pada Canvas.

using UnityEngine;
using UnityEngine.UI;

public class TampilanHud : MonoBehaviour
{
    public Text scoreText;
    public Text livesText;
    public Image[] heartIcons;

    private int score;
    private int lives = 3;

    void Start()
    {
        // Diperiksa lebih dahulu, sebab rujukan yang belum dihubungkan pada
        // Inspector merupakan penyebab kesalahan yang paling sering terjadi.
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
        }
    }

    void PerbaruiTampilan()
    {
        scoreText.text = $"Skor: {score}";
        livesText.text = $"Nyawa: {lives}";

        // Ikon nyawa dinyalakan atau dimatikan menurut sisa nyawa.
        for (int i = 0; i < heartIcons.Length; i++)
        {
            if (heartIcons[i] != null)
            {
                heartIcons[i].enabled = i < lives;
            }
        }
    }
}
