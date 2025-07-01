import React, { useState, useEffect } from 'react';

function ClosedPositionsSection() {
  const [closedPositions, setClosedPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchClosedPositions = async () => {
      try {
        const response = await fetch('/data/closed_positions');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setClosedPositions(data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchClosedPositions();
  }, []);

  if (loading) return <p>Loading closed positions...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div id="closed-positions-section" className="content-section">
      <h2>Closed Positions</h2>
      <table id="closed_positions_table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Quantity</th>
            <th>Cost</th>
            <th>Sell Price</th>
            <th>Sell Date</th>
            <th>P&L</th>
          </tr>
        </thead>
        <tbody>
          {closedPositions.map((row, index) => (
            <tr key={index}>
              <td>{row.Symbol}</td>
              <td>{row.Quantity}</td>
              <td>{row.Cost}</td>
              <td>{row['Sell Price']}</td>
              <td>{row['Sell Date']}</td>
              <td>{row['P&L']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ClosedPositionsSection;