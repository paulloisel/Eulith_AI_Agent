const API_KEY = "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"

async function fetchData() {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
            Authorization: `Bearer ${API_KEY}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [
                {
                    role: "user",
                    content: "How are you?"
                }]
        })
    })
    const data = await response.json()
    console.log(data)
}

fetchData()
