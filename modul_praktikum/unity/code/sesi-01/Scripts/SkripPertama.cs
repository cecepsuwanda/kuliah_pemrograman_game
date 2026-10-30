// SkripPertama.cs
// Skrip C# pertama: memastikan scene berjalan, lalu melaporkan keadaan
// objek setiap dua detik. Tempelkan pada GameObject "CobaSkrip".

using UnityEngine;

public class SkripPertama : MonoBehaviour
{
    // Kecepatan dalam satuan per detik, sama seperti pada Bab V.
    public float moveSpeed = 3.0f;
    public float turnSpeed = 60.0f;
    public float reportInterval = 2.0f;

    private float elapsed = 0.0f;
    private float reportTimer = 0.0f;
    private Vector3 startPosition;

    // Start dijalankan sekali, ketika scene mulai berjalan.
    void Start()
    {
        startPosition = transform.position;
        Debug.Log($"Skrip mulai. Posisi awal: {startPosition}");
    }

    // Update dijalankan sekali setiap bingkai.
    void Update()
    {
        // Selang waktu satu bingkai disediakan mesin, tidak diukur sendiri.
        float deltaTime = Time.deltaTime;

        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        Vector3 direction = new Vector3(horizontal, 0.0f, vertical);

        if (direction.magnitude > 0.01f)
        {
            // Arah dinormalkan, lalu dikalikan kecepatan dan selang waktu.
            transform.position += direction.normalized * moveSpeed * deltaTime;
        }

        transform.Rotate(0.0f, turnSpeed * deltaTime, 0.0f);

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

    // OnDisable dijalankan ketika skrip dimatikan, misalnya saat Play dihentikan.
    void OnDisable()
    {
        Debug.Log($"Skrip berhenti setelah {elapsed:F1} detik.");
    }
}
