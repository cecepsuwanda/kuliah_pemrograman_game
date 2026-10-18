// ch12_skrip_pertama.cs
// Skrip C# pertama: menggerakkan dan memutar benda, serta melaporkan kecepatan.

using UnityEngine;

public class SkripPertama : MonoBehaviour
{
    // Kecepatan dinyatakan dalam satuan per detik, sebagaimana pada Bab V.
    public float moveSpeed = 3.0f;
    public float turnSpeed = 60.0f;
    public float reportInterval = 2.0f;

    private float elapsed = 0.0f;
    private float reportTimer = 0.0f;
    private Vector3 startPosition;

    // Start dijalankan sekali, yaitu ketika scene mulai berjalan.
    void Start()
    {
        startPosition = transform.position;
        Debug.Log($"Skrip mulai. Posisi awal: {startPosition}");
    }

    // Update dijalankan sekali setiap bingkai.
    void Update()
    {
        // Selang waktu satu bingkai disediakan mesin, bukan diukur sendiri.
        float deltaTime = Time.deltaTime;

        // Gerak mendatar digerakkan tombol panah.
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        Vector3 direction = new Vector3(horizontal, 0.0f, vertical);

        if (direction.magnitude > 0.01f)
        {
            // Arah dinormalkan lebih dahulu, lalu dikalikan kecepatan dan
            // selang waktu. Urutannya sama dengan yang dipakai pada Bab V.
            transform.position += direction.normalized * moveSpeed * deltaTime;
        }

        // Benda juga diputar sedikit setiap bingkai.
        transform.Rotate(0.0f, turnSpeed * deltaTime, 0.0f);

        // Pelaporan berkala, sebagai pengganti pengukuran pada Bab IV.
        elapsed += deltaTime;
        reportTimer += deltaTime;
        if (reportTimer >= reportInterval)
        {
            reportTimer = 0.0f;
            float distance = Vector3.Distance(startPosition, transform.position);
            Debug.Log($"Waktu berjalan {elapsed:F1} detik, " +
                      $"jarak dari posisi awal {distance:F2} satuan, " +
                      $"selang bingkai {deltaTime * 1000.0f:F1} milidetik");
        }
    }

    // OnDisable dijalankan ketika skrip dimatikan, misalnya ketika berhenti
    // menjalankan scene.
    void OnDisable()
    {
        Debug.Log($"Skrip berhenti setelah {elapsed:F1} detik.");
    }
}
