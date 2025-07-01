import React, { useState, useEffect } from 'react';

function OpenPositionsSection() {
  const [openPositions, setOpenPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOpenPositions = async () => {
      try {
        const response = await fetch('/data/open_positions');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setOpenPositions(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchOpenPositions();
  }, []);

  if (loading) return <p>Loading open positions...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div id="open-positions-section" className="content-section">
      <h2>Open Positions</h2>
      <table id="open_positions_table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Portfolio %</th>
            <th>Quantity</th>
            <th>Price</th>
            <th>Cost</th>
            <th>Value</th>
            <th>P&L</th>
          </tr>
        </thead>
        <tbody>
          {openPositions.map((row, index) => (
            <tr key={index}>
              <td>{row.Symbol}</td>
              <td>{row['Portfolio %']}</td>
              <td>{row.Quantity}</td>
              <td>{row.Price}</td>
              <td>{row.Cost}</td>
              <td>{row.Value}</td>
              <td>{row['P&L']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default OpenPositionsSection;