import { useNavigate } from 'react-router-dom';
import FlightsList from './FlightsList';

function Home() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    navigate('/login');
  };

  return (
    <div className="container mt-5">
      <div className="row mb-3">
        <div className="col">
          <h1>Anasayfa</h1>
        </div>
        <div className="col text-end">
          <button className="btn btn-danger" onClick={handleLogout}>Çıkış Yap</button>
        </div>
      </div>
      <div className="row">
        <FlightsList />
      </div>
    </div>
  );
}

export default Home;