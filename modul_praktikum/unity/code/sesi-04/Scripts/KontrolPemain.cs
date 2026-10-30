// KontrolPemain.cs - kontrol pemain, Animator, dan bunyi lompat.
// Tempelkan pada "Pemain", lalu isi Ground Check, Ground Layer, Animator,
// dan Pemicu Bunyi.

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

    [Header("Animasi")]
    public Animator animator;

    [Header("Bunyi")]
    public PemicuBunyi pemicuBunyi;

    // Nama parameter harus sama persis dengan yang ada pada jendela Animator.
    private static readonly int SpeedParam = Animator.StringToHash("speed");
    private static readonly int GroundedParam = Animator.StringToHash("grounded");
    private static readonly int JumpParam = Animator.StringToHash("lompat");

    private Rigidbody2D body;
    private float inputX;
    private bool jumpRequested;
    private bool onGround;

    void Awake()
    {
        body = GetComponent<Rigidbody2D>();
    }

    void Update()
    {
        // Masukan dibaca pada Update; lompatan dibaca sebagai peristiwa.
        inputX = Input.GetAxisRaw("Horizontal");
        if (Input.GetButtonDown("Jump"))
        {
            jumpRequested = true;

            // Bunyi dipanggil di sini, pada peristiwa masukan. Memindahkannya
            // ke FixedUpdate menunda bunyi satu sampai tiga bingkai.
            if (pemicuBunyi != null) pemicuBunyi.Lompat();
        }
    }

    void FixedUpdate()
    {
        onGround = Physics2D.OverlapCircle(groundCheck.position, groundRadius,
                                           groundLayer) != null;
        // Hanya komponen mendatar yang diganti, agar gravitasi tetap bekerja.
        body.velocity = new Vector2(inputX * moveSpeed, body.velocity.y);

        if (jumpRequested && onGround)
        {
            body.velocity = new Vector2(body.velocity.x, jumpSpeed);
            if (animator != null) animator.SetTrigger(JumpParam);
        }
        jumpRequested = false;

        if (animator != null)
        {
            animator.SetFloat(SpeedParam, Mathf.Abs(body.velocity.x));
            animator.SetBool(GroundedParam, onGround);
        }
    }

    void OnDrawGizmosSelected()
    {
        if (groundCheck == null) return;
        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(groundCheck.position, groundRadius);
    }
}
