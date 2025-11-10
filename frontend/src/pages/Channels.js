import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import {
  getChannels,
  getFacebookAuthUrl,
  getInstagramAuthUrl,
  getLinkedInAuthUrl,
  getTikTokAuthUrl,
  syncMessages,
  deleteChannel,
} from '../services/channels';

function Channels() {
  const [channels, setChannels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    loadChannels();

    // Check for OAuth success
    const success = searchParams.get('success');
    if (success) {
      setSuccessMessage(`Canale ${success} connesso con successo!`);
      setTimeout(() => setSuccessMessage(''), 5000);
    }
  }, [searchParams]);

  const loadChannels = async () => {
    try {
      const data = await getChannels();
      setChannels(data.results || data);
    } catch (error) {
      console.error('Errore nel caricamento dei canali:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleConnectChannel = async (platform) => {
    try {
      let authUrl;
      switch (platform) {
        case 'facebook':
          authUrl = await getFacebookAuthUrl();
          break;
        case 'instagram':
          authUrl = await getInstagramAuthUrl();
          break;
        case 'linkedin':
          authUrl = await getLinkedInAuthUrl();
          break;
        case 'tiktok':
          authUrl = await getTikTokAuthUrl();
          break;
        default:
          return;
      }
      window.location.href = authUrl;
    } catch (error) {
      console.error('Errore nella connessione:', error);
      alert('Errore durante la connessione al canale');
    }
  };

  const handleSync = async (channelId) => {
    try {
      await syncMessages(channelId);
      alert('Sincronizzazione avviata!');
    } catch (error) {
      console.error('Errore nella sincronizzazione:', error);
      alert('Errore durante la sincronizzazione');
    }
  };

  const handleDelete = async (channelId) => {
    if (window.confirm('Sei sicuro di voler disconnettere questo canale?')) {
      try {
        await deleteChannel(channelId);
        loadChannels();
      } catch (error) {
        console.error('Errore nella disconnessione:', error);
        alert('Errore durante la disconnessione');
      }
    }
  };

  const getPlatformName = (platform) => {
    const names = {
      facebook: 'Facebook',
      instagram: 'Instagram',
      linkedin: 'LinkedIn',
      tiktok: 'TikTok',
    };
    return names[platform] || platform;
  };

  const isConnected = (platform) => {
    return channels.some((channel) => channel.platform === platform);
  };

  return (
    <div>
      <Navbar />
      <div className="container">
        <h2 style={{ marginBottom: '30px' }}>Gestione Canali</h2>

        {successMessage && (
          <div className="success-message">{successMessage}</div>
        )}

        <div className="card">
          <h3>Connetti Nuovi Canali</h3>
          <div className="social-icons">
            <button
              className={`social-icon-btn ${isConnected('facebook') ? 'connected' : ''}`}
              onClick={() => handleConnectChannel('facebook')}
              disabled={isConnected('facebook')}
            >
              Facebook {isConnected('facebook') && '✓'}
            </button>
            <button
              className={`social-icon-btn ${isConnected('instagram') ? 'connected' : ''}`}
              onClick={() => handleConnectChannel('instagram')}
              disabled={isConnected('instagram')}
            >
              Instagram {isConnected('instagram') && '✓'}
            </button>
            <button
              className={`social-icon-btn ${isConnected('linkedin') ? 'connected' : ''}`}
              onClick={() => handleConnectChannel('linkedin')}
              disabled={isConnected('linkedin')}
            >
              LinkedIn {isConnected('linkedin') && '✓'}
            </button>
            <button
              className={`social-icon-btn ${isConnected('tiktok') ? 'connected' : ''}`}
              onClick={() => handleConnectChannel('tiktok')}
              disabled={isConnected('tiktok')}
            >
              TikTok {isConnected('tiktok') && '✓'}
            </button>
          </div>
        </div>

        <div className="card">
          <h3>Canali Connessi</h3>
          {loading ? (
            <p>Caricamento...</p>
          ) : channels.length === 0 ? (
            <p style={{ color: '#666' }}>Nessun canale connesso</p>
          ) : (
            <div>
              {channels.map((channel) => (
                <div
                  key={channel.id}
                  style={{
                    padding: '15px',
                    borderBottom: '1px solid #eee',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <div>
                    <h4>{getPlatformName(channel.platform)}</h4>
                    <p style={{ color: '#666', fontSize: '14px' }}>
                      {channel.platform_username || channel.platform_user_id}
                    </p>
                    <p style={{ fontSize: '12px', color: '#999' }}>
                      Ultima sincronizzazione:{' '}
                      {channel.last_sync_at
                        ? new Date(channel.last_sync_at).toLocaleString('it-IT')
                        : 'Mai'}
                    </p>
                  </div>
                  <div>
                    <button
                      className="btn btn-small btn-secondary"
                      onClick={() => handleSync(channel.id)}
                    >
                      Sincronizza
                    </button>
                    <button
                      className="btn btn-small"
                      style={{ background: '#dc3545', marginLeft: '10px' }}
                      onClick={() => handleDelete(channel.id)}
                    >
                      Disconnetti
                    </button>
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

export default Channels;
