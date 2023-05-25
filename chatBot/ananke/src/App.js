import { useState, useEffect} from "react"


const App = () => {
  const [value, setValue] = useState(null)
  const [message, setMessage] = useState(null)

  const getMessages = async () => {
    const options = {
      method: "POST",
      body: JSON.stringify({
        message: value
      }),
      headers: {
        "Content-Type": "application/json"
      }
    }
    try {
      const response = await fetch('http://localhost:8000/completions', options)
      const data = await response.json()
      setMessage(data.choices[0].message)
    } catch (error) {
      console.error(error)
    }
  }

  console.log(message)
  return (
    <div className="app">
      <section className="side-bar">
        <button>+ New chat</button>
        <ul className="history">
          <li>BUGH</li>
        </ul>
        <nav>
          <p>Made by Paul</p>
        </nav>
      </section>
      <section className="main">
        <h1>Ananke</h1>
        <ul className="feed">

        </ul>
        <div className="bottom-section">
          <div className="input-container">
            <input value={value} onChange={(e) => setValue(e.target.value)}/>
            <div id="submit" onClick={getMessages}>➢</div>
          </div>
          <p className="info">
            Powered by OpenAI API based on ChatGPT May 12 Version
          </p>
        </div>
      </section>
    </div>
  )
}

export default App
