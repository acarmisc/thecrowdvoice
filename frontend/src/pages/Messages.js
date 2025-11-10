import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { getMessages, batchAnalyze } from '../services/messages';

function Messages() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [filter, setFilter] = useState({
    platform: '',
    type: '',
  });

  useEffect(() => {
    loadMessages();
  }, [filter]);

  const loadMessages = async () => {
    setLoading(true);
    try {
      const params = {};
      if (filter.platform) params.platform = filter.platform;
      if (filter.type) params.type = filter.type;

      const data = await getMessages(params);
      setMessages(data.results || data);
    } catch (error) {
      console.error('Errore nel caricamento dei messaggi:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBatchAnalyze = async () => {
    setAnalyzing(true);
    try {
      const result = await batchAnalyze();
      alert(`Analizzati ${result.analyzed} messaggi`);
      loadMessages();
    } catch (error) {
      console.error('Errore nell\'analisi:', error);
      alert('Errore durante l\'analisi');
    } finally {
      setAnalyzing(false);
    }
  };

  const getSentimentBadge = (sentiment) => {
    if (!sentiment) return null;

    const className = `sentiment-badge sentiment-${sentiment.label}`;
    return <span className={className}>{sentiment.label}</span>;
  };

  const getMessageTypeLabel = (type) => {
    const labels = {
      direct_message: 'Messaggio Diretto',
      comment: 'Commento',
      mention: 'Menzione',
      tag: 'Tag',
      reply: 'Risposta',
    };
    return labels[type] || type;
  };

  return (
    <div>
      <Navbar />
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
          <h2>Messaggi e Interazioni</h2>
          <button
            className="btn btn-small"
            onClick={handleBatchAnalyze}
            disabled={analyzing}
          >
            {analyzing ? 'Analisi in corso...' : 'Analizza Tutti'}
          </button>
        </div>

        <div className="card">
          <div style={{ display: 'flex', gap: '15px', marginBottom: '20px' }}>
            <div>
              <label style={{ marginRight: '10px' }}>Piattaforma:</label>
              <select
                value={filter.platform}
                onChange={(e) => setFilter({ ...filter, platform: e.target.value })}
                style={{ padding: '8px', borderRadius: '5px', border: '1px solid #ddd' }}
              >
                <option value="">Tutte</option>
                <option value="facebook">Facebook</option>
                <option value="instagram">Instagram</option>
                <option value="linkedin">LinkedIn</option>
                <option value="tiktok">TikTok</option>
              </select>
            </div>
            <div>
              <label style={{ marginRight: '10px' }}>Tipo:</label>
              <select
                value={filter.type}
                onChange={(e) => setFilter({ ...filter, type: e.target.value })}
                style={{ padding: '8px', borderRadius: '5px', border: '1px solid #ddd' }}
              >
                <option value="">Tutti</option>
                <option value="direct_message">Messaggi Diretti</option>
                <option value="comment">Commenti</option>
                <option value="mention">Menzioni</option>
                <option value="tag">Tag</option>
                <option value="reply">Risposte</option>
              </select>
            </div>
          </div>

          {loading ? (
            <p>Caricamento...</p>
          ) : messages.length === 0 ? (
            <p style={{ color: '#666', textAlign: 'center', padding: '40px' }}>
              Nessun messaggio trovato. Sincronizza i tuoi canali per ricevere messaggi.
            </p>
          ) : (
            <div className="messages-list">
              {messages.map((message) => (
                <div key={message.id} className="message-item">
                  <div className="message-header">
                    <span>
                      <strong>{message.sender_name || message.sender_username}</strong> •{' '}
                      {message.platform} • {getMessageTypeLabel(message.message_type)}
                    </span>
                    <span>{new Date(message.received_at).toLocaleString('it-IT')}</span>
                  </div>
                  <div className="message-text">{message.text}</div>
                  <div>
                    {message.sentiment ? (
                      getSentimentBadge(message.sentiment)
                    ) : (
                      <span style={{ fontSize: '12px', color: '#999' }}>
                        Non ancora analizzato
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Messages;
