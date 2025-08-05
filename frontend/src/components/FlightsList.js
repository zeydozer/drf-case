import { useState, useEffect } from 'react';
import axios from 'axios';

function FlightsList() {
  const [flights, setFlights] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('access');
    if (!token) {
      setError('Lütfen giriş yapın.');
      return;
    }
    axios.get('http://localhost/api/flights/', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }).then(response => {
      setFlights(response.data);
    }).catch(err => {
      setError('Uçuşlar alınırken bir hata oluştu.');
    });
  }, []);

  if (error) 
    return <div className="alert alert-danger mt-3">{error}</div>;

  return (
    <div className="container">
      <h2>Uçuşlar</h2>
      <table className="table table-striped mt-3">
        <thead>
          <tr>
            <th>#</th>
            <th>Uçuş No</th>
            <th>Nereden</th>
            <th>Nereye</th>
            <th>Zaman</th>
            <th>Durum</th>
          </tr>
        </thead>
        <tbody>
          {flights.map((flight, i) => (
            <tr key={flight.id || i}>
              <td>{i + 1}</td>
              <td>{flight.flight_number}</td>
              <td>{flight.origin}</td>
              <td>{flight.destination}</td>
              <td>{flight.scheduled_time}</td>
              <td>{flight.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FlightsList;