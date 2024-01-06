import './App.css'

import React, { useState, useEffect } from 'react';

const App = () => {
  const [albums, setAlbums] = useState([]);
  const [gridSize, setGridSize] = useState(5);
  const [sortMethod, setSortMethod] = useState('year');
  const [sortOrder, setSortOrder] = useState('ascending');
  const host = !process.env.NODE_ENV || process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : '';
  
  useEffect(() => {
    fetch(`${host}/api`)
         .then((response) => response.json())
         .then((data) => {
            setAlbums(data);
         }) 
         .catch((err) => {
            console.log(err.message);
         });
  }, []);

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
    }
    return 0
  })

  const itemStyle = {
    width: gridSize * 50
  }

  const imgStyle = {
    maxWidth: gridSize * 50,
    maxHeight: gridSize * 50
  }

  return (
    <div className="App">
      <select
        value={sortMethod}
        onChange={e => setSortMethod(e.target.value)}
      >
        <option value="year">year</option>
        <option value="artist">artist</option>
      </select>

      <select
        value={sortOrder}
        onChange={e => setSortOrder(e.target.value)}
      >
        <option value="ascending">ascending</option>
        <option value="descending">descending</option>
      </select>

      <input
        type="range" 
        name="size"
        min="1" max="10" 
        value={gridSize}
        onChange={e => setGridSize(e.target.value)}
      />

      <div className='container'>
        {albums.sort(compareAlbums).map((album) => {
          return (
            <div className="item" style={itemStyle} key={album.id}>
              {album.artwork === true &&
                <img
                  alt={album.name}
                  src={`${host}/static/img/${album.id}.jpg`}
                  style={imgStyle}
                />
              }
            </div>
          )
        })}
      </div>
    </div>
  );
}

export default App;
