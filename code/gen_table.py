def generate_genre_table():
    header = r"""
\begin{table}[h]
    \centering
    \caption{Ringkasan Genre Game Utama}
    \label{tab:genre_summary}
    \begin{tabularx}{\textwidth}{|l|X|l|}
        \hline
        \textbf{Genre} & \textbf{Karakteristik Utama} & \textbf{Contoh Populer} \\
        \hline
        Action & Fokus refleks, koordinasi tangan-mata, combat & CoD, Devil May Cry \\
        \hline
        Adventure & Narasi, eksplorasi, puzzle-solving & Zelda, Uncharted \\
        \hline
        RPG & Pengembangan karakter, statistik, cerita & Final Fantasy, Skyrim \\
        \hline
        Strategy & Perencanaan, taktik, resource management & Civilization, StarCraft \\
        \hline
        Simulation & Realisme, meniru dunia nyata & The Sims, Flight Sim \\
        \hline
        Sports & Kompetisi olahraga, realisme fisik & FIFA, NBA 2K \\
        \hline
        Puzzle & Logika, pemecahan masalah & Tetris, Portal \\
        \hline
        Platformer & Navigasi, melompat, presisi & Super Mario, Celeste \\
        \hline
    \end{tabularx}
\end{table}
"""
    return header

print(generate_genre_table())
