import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { getChannels } from '../services/channels';
import { getMessages, getSentimentStats } from '../services/messages';

function Dashboard() {
  const [stats, setStats] = useState({
    channels: 0,
    messages: 0,
    sentiment: {
      total: 0,
      positive: 0,
      negative: 0,
      neutral: 0,
    },
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [channelsData, messagesData, sentimentData] = await Promise.all([
        getChannels(),
        getMessages(),
        getSentimentStats(),
      ]);

      setStats({
        channels: channelsData.results?.length || channelsData.length || 0,
        messages: messagesData.count || messagesData.results?.length || 0,
        sentiment: sentimentData,
      });
    } catch (error) {
      console.error('Errore nel caricamento dei dati:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Navbar />
      <div className="container">
        <h2 style={{ marginBottom: '30px' }}>Dashboard</h2>

        {loading ? (
          <p>Caricamento...</p>
        ) : (
          <>
            <div className="stats-grid">
              <div className="stat-card">
                <h4>{stats.channels}</h4>
                <p>Canali Connessi</p>
              </div>
              <div className="stat-card">
                <h4>{stats.messages}</h4>
                <p>Messaggi Totali</p>
              </div>
              <div className="stat-card">
                <h4>{stats.sentiment.total}</h4>
                <p>Messaggi Analizzati</p>
              </div>
            </div>

            <div className="card">
              <h3>Analisi Sentiment</h3>
              <div className="stats-grid">
                <div className="stat-card" style={{ background: '#d4edda' }}>
                  <h4>{stats.sentiment.positive}</h4>
                  <p>Positivi ({stats.sentiment.positive_percentage?.toFixed(1)}%)</p>
                </div>
                <div className="stat-card" style={{ background: '#f8d7da' }}>
                  <h4>{stats.sentiment.negative}</h4>
                  <p>Negativi ({stats.sentiment.negative_percentage?.toFixed(1)}%)</p>
                </div>
                <div className="stat-card" style={{ background: '#e2e3e5' }}>
                  <h4>{stats.sentiment.neutral}</h4>
                  <p>Neutrali ({stats.sentiment.neutral_percentage?.toFixed(1)}%)</p>
                </div>
              </div>
            </div>

            {stats.channels === 0 && (
              <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
                <h3>Inizia connettendo un canale social</h3>
                <p style={{ marginBottom: '20px', color: '#666' }}>
                  Collega i tuoi account social per iniziare a ricevere e analizzare le interazioni
                </p>
                <a href="/channels" className="btn btn-small">
                  Aggiungi Canale
                </a>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
