// AnimasiPemain.cs - membalik arah hadap gambar menurut arah gerak.
// Tempelkan pada "Pemain" bersama KontrolPemain.

using UnityEngine;

public class AnimasiPemain : MonoBehaviour
{
    public Rigidbody2D body;
    public float ambangGerak = 0.1f;
    private bool hadapKanan = true;

    void Awake()
    {
        if (body == null) body = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        if (body == null) return;
        float arah = body.velocity.x;
        if (Mathf.Abs(arah) < ambangGerak) return;

        bool kanan = arah > 0.0f;
        if (kanan == hadapKanan) return;
        hadapKanan = kanan;

        // Gambar dibalik melalui skala, bukan diputar 180 derajat.
        Vector3 skala = transform.localScale;
        skala.x = Mathf.Abs(skala.x) * (kanan ? 1.0f : -1.0f);
        transform.localScale = skala;
    }
}
