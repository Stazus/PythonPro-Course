import { useState } from "react";


function App() {
    const [preferences, setPreferences] = useState("");
    const [message, setMessage] = useState("");
    const [recommendations, setRecommendations] = useState([]);


    const sleep = (milliseconds) => {
        return new Promise(
            (resolve) => setTimeout(resolve, milliseconds)
        );
    };


    const waitForResult = async (taskId) => {
        for (let attempt = 0; attempt < 60; attempt++) {
            await sleep(1000);

            const response = await fetch(
                `/api/result/${taskId}`
            );

            if (!response.ok) {
                throw new Error("Błąd pobierania wyniku");
            }

            const data = await response.json();

            if (data.status === "SUCCESS") {
                setRecommendations(data.recommendations);
                setMessage("Gotowe.");
                return;
            }

            if (data.status === "FAILURE") {
                throw new Error(
                    data.error || "Zadanie AI zakończyło się błędem"
                );
            }
        }

        throw new Error("Przekroczono czas oczekiwania");
    };


    const getRecommendation = async () => {
        if (!preferences.trim()) {
            setMessage("Wpisz swoje preferencje.");
            return;
        }

        setRecommendations([]);
        setMessage("Uruchamiam analizę AI...");

        try {
            const response = await fetch(
                "/api/recommend",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        preferences,
                    }),
                }
            );

            if (!response.ok) {
                throw new Error("Błąd backendu");
            }

            const data = await response.json();

            if (data.cached) {
                setRecommendations(
                    data.recommendations
                );

                setMessage(
                    "Gotowe. Wynik pobrany z cache Redis."
                );

                return;
            }

            setMessage(
                "AI analizuje preferencje..."
            );

            await waitForResult(
                data.task_id
            );

        } catch (error) {
            setMessage(
                `Błąd: ${error.message}`
            );
        }
    };


    return (
        <div
            style={{
                maxWidth: "700px",
                margin: "60px auto",
                fontFamily: "Arial, sans-serif",
            }}
        >
            <h1>AI Book Recommendations</h1>

            <p>
                Opisz książki, autorów lub gatunki,
                które lubisz.
            </p>

            <textarea
                rows="7"
                style={{
                    width: "100%",
                    padding: "10px",
                }}
                value={preferences}
                onChange={(event) =>
                    setPreferences(event.target.value)
                }
                placeholder="Np. Lubię fantastykę, podróże w czasie i powieści historyczne..."
            />

            <br />
            <br />

            <button
                onClick={getRecommendation}
            >
                Znajdź rekomendacje
            </button>

            <p>{message}</p>

            {recommendations.length > 0 && (
                <div>
                    <h2>Rekomendowane książki</h2>

                    <ol>
                        {recommendations.map(
                            (book) => (
                                <li
                                    key={`${book.title}-${book.author}`}
                                    style={{
                                        marginBottom: "12px",
                                    }}
                                >
                                    <strong>
                                        {book.title}
                                    </strong>
                                    {" — "}
                                    {book.author}
                                    <br />
                                    Dopasowanie:{" "}
                                    {(
                                        book.score * 100
                                    ).toFixed(1)}
                                    %
                                </li>
                            )
                        )}
                    </ol>
                </div>
            )}
        </div>
    );
}


export default App;
