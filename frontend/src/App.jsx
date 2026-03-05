import { useState, useRef, useEffect } from 'react'

function App() {
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const sendMessage = async (e) => {
        e.preventDefault()
        if (!input.trim() || loading) return

        const query = input.trim()
        setInput('')
        setMessages(prev => [...prev, { role: 'user', content: query }])
        setLoading(true)

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query }),
            })

            if (!res.ok) {
                const err = await res.json()
                throw new Error(err.detail || 'Chat request failed')
            }

            const data = await res.json()
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: data.response,
                citations: data.citations,
                context_tokens: data.context_tokens_used,
            }])
        } catch (err) {
            setMessages(prev => [...prev, {
                role: 'error',
                content: `Error: ${err.message}`,
            }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app">
            <header className="header">
                <div className="header-content">
                    <h1>⚙️ GusEngine</h1>
                    <span className="subtitle">Automotive Diagnostic RAG — Prototype</span>
                </div>
            </header>

            <main className="chat-container">
                <div className="messages">
                    {messages.length === 0 && (
                        <div className="empty-state">
                            <div className="empty-icon">🔧</div>
                            <h2>Ready for diagnostics</h2>
                            <p>Ask a question about your ingested FSM documents.</p>
                            <div className="example-queries">
                                <button onClick={() => setInput('What is the torque spec for the front brake caliper bolts?')}>
                                    Brake caliper torque specs
                                </button>
                                <button onClick={() => setInput('How do I diagnose a P0300 random misfire code?')}>
                                    P0300 misfire diagnosis
                                </button>
                                <button onClick={() => setInput('What is the recommended oil type and capacity?')}>
                                    Oil specifications
                                </button>
                            </div>
                        </div>
                    )}

                    {messages.map((msg, i) => (
                        <div key={i} className={`message ${msg.role}`}>
                            <div className="message-content">
                                {msg.role === 'user' && <div className="message-label">You</div>}
                                {msg.role === 'assistant' && <div className="message-label">Gus</div>}
                                {msg.role === 'error' && <div className="message-label">⚠️ Error</div>}
                                <div className="message-text">{msg.content}</div>
                                {msg.citations && msg.citations.length > 0 && (
                                    <div className="citations">
                                        <div className="citations-label">Sources:</div>
                                        {msg.citations.map((cite, j) => (
                                            <a key={j} className="citation" href={`/pdfs/${cite.source}`} target="_blank" rel="noreferrer">
                                                📄 {cite.source}
                                                {cite.page_numbers.length > 0 && ` (p. ${cite.page_numbers.join(', ')})`}
                                            </a>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="message assistant">
                            <div className="message-content">
                                <div className="message-label">Gus</div>
                                <div className="loading-dots">
                                    <span></span><span></span><span></span>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </main>

            <footer className="input-area">
                <form onSubmit={sendMessage} className="input-form">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask Gus a diagnostic question..."
                        disabled={loading}
                        autoFocus
                    />
                    <button type="submit" disabled={loading || !input.trim()}>
                        {loading ? '⏳' : '→'}
                    </button>
                </form>
            </footer>
        </div>
    )
}

export default App
