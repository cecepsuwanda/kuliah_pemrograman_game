// ch14_kontrol_animasi.cs
// Menghubungkan keadaan pemain dengan animasi melalui Animator.

using UnityEngine;

public class KontrolAnimasi : MonoBehaviour
{
    public Animator animator;
    public Rigidbody2D body;
    public float runThreshold = 0.1f;

    // Nama parameter harus sama persis dengan yang dibuat pada jendela
    // Animator, sebab kesamaannya tidak diperiksa oleh penyunting.
    private static readonly int SpeedParam = Animator.StringToHash("speed");
    private static readonly int GroundedParam = Animator.StringToHash("grounded");

    private KontrolPemain kontrol;

    void Awake()
    {
        if (animator == null)
        {
            animator = GetComponent<Animator>();
        }
        if (body == null)
        {
            body = GetComponent<Rigidbody2D>();
        }
        kontrol = GetComponent<KontrolPemain>();
    }

    void Update()
    {
        if (animator == null || body == null)
        {
            return;
        }

        // Kecepatan mendatar diteruskan ke Animator sebagai angka.
        float speed = Mathf.Abs(body.velocity.x);
        animator.SetFloat(SpeedParam, speed);

        // Keadaan menyentuh tanah diteruskan sebagai nilai benar atau salah.
        // Nilainya diambil dari skrip kontrol pemain, bila tersedia.
        bool grounded = kontrol != null ? kontrol.IsOnGround : true;
        animator.SetBool(GroundedParam, grounded);

        // Membalik arah hadap gambar menurut arah geraknya.
        if (speed > runThreshold)
        {
            Vector3 scale = transform.localScale;
            scale.x = body.velocity.x < 0.0f
                ? -Mathf.Abs(scale.x)
                : Mathf.Abs(scale.x);
            transform.localScale = scale;
        }
    }
}
