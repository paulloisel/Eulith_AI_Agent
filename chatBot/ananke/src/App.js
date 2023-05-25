const App = () => {
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
            <input/>
            <div id="submit">➢</div>
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
