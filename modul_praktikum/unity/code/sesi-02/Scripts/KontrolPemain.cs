// KontrolPemain.cs
// Kontrol pemain Level Rak berbasis Rigidbody2D.
// Tempelkan pada GameObject "Pemain", lalu isi Ground Check dan Ground Layer
// pada Inspector.

using UnityEngine;

[RequireComponent(typeof(Rigidbody2D))]
public class KontrolPemain : MonoBehaviour
{
    [Header("Gerak")]
    public float moveSpeed = 6.0f;
    public float jumpSpeed = 11.0f;

    [Header("Pemeriksaan tanah")]
    public Transform groundCheck;
    public float groundRadius = 0.15f;
    public LayerMask groundLayer;

    private Rigidbody2D body;
    private float inputX;
    private bool jumpRequested;
    private bool onGround;

    // Keadaan menyentuh tanah dibuka bagi skrip lain.
    public bool IsOnGround
    {
        get { return onGround; }
    }

    void Awake()
    {
        // Rujukan komponen diambil sekali saja, bukan setiap bingkai.
        body = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        // Masukan dibaca pada Update, sebab nilainya dapat berubah beberapa
        // kali dalam satu bingkai fisika.
        inputX = Input.GetAxisRaw("Horizontal");

        // Lompatan dibaca sebagai peristiwa, bukan sebagai keadaan tombol.
        if (Input.GetButtonDown("Jump"))
        {
            jumpRequested = true;
        }
    }

    void FixedUpdate()
    {
        // Pemeriksaan tanah dan gerak dikerjakan pada FixedUpdate, sebab
        // keduanya berkaitan dengan perhitungan fisika.
        onGround = Physics2D.OverlapCircle(groundCheck.position, groundRadius,
                                           groundLayer) != null;

        // Hanya komponen mendatar yang diganti. Komponen tegak dibiarkan
        // agar gravitasi tetap bekerja.
        // Catatan: pada Unity 6, velocity berganti nama menjadi linearVelocity.
        body.velocity = new Vector2(inputX * moveSpeed, body.velocity.y);

        if (jumpRequested && onGround)
        {
            body.velocity = new Vector2(body.velocity.x, jumpSpeed);
        }
        jumpRequested = false;
    }

    // Menggambar lingkaran pemeriksaan tanah pada tampilan Scene.
    void OnDrawGizmosSelected()
    {
        if (groundCheck == null)
        {
            return;
        }
        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(groundCheck.position, groundRadius);
    }
}
