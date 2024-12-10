import React, { useState } from 'react';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [artistInfo, setArtistInfo] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!searchTerm) return;

    setLoading(true);

    try {
      // Fetch artist info from Flask backend
      const response = await fetch(`http://localhost:5000/search?q=${searchTerm}`);
      const data = await response.json();

      if (data.error) {
        alert(data.error);
        setArtistInfo(null);
      } else {
        setArtistInfo(data);
      }
    } catch (error) {
      console.error('Error fetching artist:', error);
      alert('Error fetching artist data.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddArtist = async () => {
    if (!artistInfo) return;

    try {
      // Add artist to the backend database
      const response = await fetch('http://localhost:5000/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          artist_id: artistInfo.id,
          album_length: artistInfo.album_length,
          image_url: artistInfo.image_url,
        }),
      });

      const data = await response.json();

      if (data.message) {
        alert(data.message);
      }
    } catch (error) {
      console.error('Error adding artist:', error);
      alert('Error adding artist to the database.');
    }
  };

  return (
    <div className="App">
      <h1>Artist Search</h1>
      <input
        type="text"
        placeholder="Search for an artist..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      {loading && <p>Loading...</p>}

      {artistInfo && (
        <div>
          <h2>{artistInfo.name}</h2>
          {artistInfo.image_url && <img src={artistInfo.image_url} alt={artistInfo.name} width="200" />}
          <p>Album count: {artistInfo.album_length}</p>
          <button onClick={handleAddArtist}>Add to Database</button>
        </div>
      )}
    </div>
  );
}

export default App;