import './App.css'
import GridItem from './GridItem';

import React, { useState, useEffect } from 'react';

const App = () => {
  const [loading, setLoading] = useState(true);
  const [library, setLibrary] = useState([]);
  const [sortMethod, setSortMethod] = useState(localStorage.getItem('sortMethod') || 'year');
  const [sortOrder, setSortOrder] = useState(localStorage.getItem('sortOrder') || 'ascending');
  const [gridSize, setGridSize] = useState(localStorage.getItem('gridSize') || 5);
  const host = !process.env.NODE_ENV || process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : '';

  useEffect(() => {
    localStorage.setItem('sortMethod', sortMethod);
  }, [sortMethod]);

  useEffect(() => {
    localStorage.setItem('sortOrder', sortOrder);
  }, [sortOrder]);

  useEffect(() => {
    localStorage.setItem('gridSize', gridSize);
  }, [gridSize]);
  
  useEffect(() => {
    fetch(`${host}/api`)
         .then((response) => response.json())
         .then((data) => {
            setLibrary(data);
            setLoading(false);
         }) 
         .catch((err) => {
            console.log(err.message);
         });
  }, [host]);

  const compareAlbums = ((a, b) => {
    if (sortOrder === 'descending') {
      [a, b] = [b, a];
    }
    switch (sortMethod) {
      case 'year':
        return a.year - b.year;
      case 'artist':
        if (a.artist < b.artist) {
          return -1;
        }
        if (a.artist > b.artist) {
          return 1; 
        }
        return 0
      case 'random':
        return Math.random() - 0.5
      default:
        return 0
    }
  })

  const playAlbum = (album) => {
    fetch(`${host}/api`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ album })
    })
         .then((response) => response.json())
         .then((data) => {
            console.log(data)
         }) 
         .catch((err) => {
            console.log(err.message);
         });
  }

  return (
    <div className="App">
      <div className="toolbar">
        <select
          name="sort-method"
          value={sortMethod}
          onChange={e => setSortMethod(e.target.value)}
        >
          <option value="year">year</option>
          <option value="artist">artist</option>
          <option value="random">random</option>
        </select>
        <select
          name="sort-order"
          value={sortOrder}
          onChange={e => setSortOrder(e.target.value)}
        >
          <option value="ascending">ascending</option>
          <option value="descending">descending</option>
        </select>
        <input
          type="range" 
          name="size"
          min="1" max="9" 
          value={gridSize}
          onChange={e => setGridSize(e.target.value)}
        />
        {loading && <span className='loader'>Loading library...</span>}
      </div>
      <div className='container'>
        {library.sort(compareAlbums).map((album) => 
          <GridItem
            key={album.id}
            album={album}
            gridSize={gridSize}
            host={host}
            onClick={e => {playAlbum(album.name)}}
          />
        )}
      </div>
    </div>
  );
}

export default App;
