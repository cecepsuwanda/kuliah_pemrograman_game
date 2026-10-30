// ManajerBunyi.cs - pemusat musik latar dan efek suara.
// Tempelkan pada GameObject "ManajerBunyi" yang memuat dua AudioSource.

using UnityEngine;

public class ManajerBunyi : MonoBehaviour
{
    // Satu salinan yang hidup selama permainan berlangsung.
    public static ManajerBunyi Instance;

    [Header("Sumber bunyi")]
    public AudioSource musicSource;   // memutar musik latar berulang
    public AudioSource sfxSource;     // memainkan efek suara sekali pakai

    [Header("Klip")]
    public AudioClip musikLatar;
    public AudioClip bunyiLompat;
    public AudioClip bunyiAmbil;
    public AudioClip bunyiKalah;

    [Header("Kekuatan")]
    [Range(0.0f, 1.0f)] public float volumeMusik = 0.4f;
    [Range(0.0f, 1.0f)] public float volumeEfek = 0.8f;
    [Range(0.0f, 0.3f)] public float variasiNada = 0.08f;

    void Awake()
    {
        // Salinan lama dibuang apabila scene dimuat ulang, supaya musik
        // tidak menumpuk menjadi dua.
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
        if (musicSource == null || musikLatar == null) return;

        musicSource.clip = musikLatar;
        musicSource.loop = true;
        musicSource.volume = volumeMusik;
        musicSource.Play();
    }

    public void Efek(AudioClip klip)
    {
        if (sfxSource == null || klip == null) return;

        // Nada digeser sedikit agar bunyi yang dipanggil berulang tidak
        // terdengar seperti mesin.
        sfxSource.pitch = 1.0f + Random.Range(-variasiNada, variasiNada);
        sfxSource.PlayOneShot(klip, volumeEfek);
    }

    public void BunyiLompat() { Efek(bunyiLompat); }
    public void BunyiAmbil() { Efek(bunyiAmbil); }

    public void BunyiKalah()
    {
        if (musicSource != null) musicSource.Stop();
        Efek(bunyiKalah);
    }
}
