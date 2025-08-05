import React from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    navigate('/login');
  };

  return (
    <div className="container mt-5">
      <h1>Anasayfa</h1>
      <button className="btn btn-danger mt-3" onClick={handleLogout}>
        Çıkış Yap
      </button>
    </div>
  );
}

export default Home;