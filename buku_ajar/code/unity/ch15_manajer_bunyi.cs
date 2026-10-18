// ch15_manajer_bunyi.cs
// Pemusat bunyi permainan: musik latar (BGM) dan efek suara (SFX).

using UnityEngine;

public class ManajerBunyi : MonoBehaviour
{
    // Satu-satunya salinan yang hidup selama permainan berlangsung.
    public static ManajerBunyi Instance;

    public AudioSource musicSource;   // memutar BGM secara berulang
    public AudioSource sfxSource;     // memainkan SFX sekali pakai

    public AudioClip backgroundMusic;
    public AudioClip jumpSound;
    public AudioClip pickupSound;
    public AudioClip hurtSound;
    public AudioClip gameOverSound;

    public float musicVolume = 0.5f;
    public float sfxVolume = 0.8f;
    public float pitchVariation = 0.08f;

    void Awake()
    {
        // Apabila scene dimuat ulang, salinan lama dibuang supaya bunyinya
        // tidak menumpuk.
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }

        Instance = this;
        DontDestroyOnLoad(gameObject);

        if (musicSource == null || sfxSource == null)
        {
            Debug.LogWarning("Sumber bunyi belum dihubungkan pada Inspector.");
            enabled = false;
        }
    }

    void Start()
    {
        PutarMusik();
    }

    // --- Bagian yang dipanggil oleh skrip lain ------------------------

    public void PutarMusik()
    {
        if (musicSource == null || backgroundMusic == null) return;

        musicSource.clip = backgroundMusic;
        musicSource.loop = true;
        musicSource.volume = musicVolume;
        musicSource.Play();
    }

    public void HentikanMusik()
    {
        if (musicSource != null) musicSource.Stop();
    }

    // PlayOneShot dipakai untuk SFX, sebab beberapa bunyi dapat berbunyi
    // bersamaan tanpa saling memotong.
    public void Efek(AudioClip klip)
    {
        if (sfxSource == null || klip == null) return;

        // Nada digeser sedikit setiap kali, supaya bunyi yang sama tidak
        // terdengar seperti mesin ketika dipanggil berulang dengan cepat.
        sfxSource.pitch = 1.0f + Random.Range(-pitchVariation, pitchVariation);
        sfxSource.PlayOneShot(klip, sfxVolume);
    }

    public void BunyiLompat() { Efek(jumpSound); }
    public void BunyiAmbil() { Efek(pickupSound); }
    public void BunyiTerluka() { Efek(hurtSound); }

    public void BunyiKalah()
    {
        HentikanMusik();
        Efek(gameOverSound);
    }
}
