import React, { useState, useEffect } from 'react';

function PortfolioValuesSection() {
  const [portfolioValues, setPortfolioValues] = useState([]);
  const [advancedMetrics, setAdvancedMetrics] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPortfolioData = async () => {
      try {
        // Fetch portfolio values
        const portfolioValuesResponse = await fetch('/data/portfolio_value');
        if (!portfolioValuesResponse.ok) {
          throw new Error(`HTTP error! status: ${portfolioValuesResponse.status}`);
        }
        const portfolioValuesData = await portfolioValuesResponse.json();
        setPortfolioValues(portfolioValuesData);

        // Fetch advanced metrics
        const advancedMetricsResponse = await fetch('/data/metrics/advanced');
        if (!advancedMetricsResponse.ok) {
          throw new Error(`HTTP error! status: ${advancedMetricsResponse.status}`);
        }
        const advancedMetricsData = await advancedMetricsResponse.json();
        setAdvancedMetrics(advancedMetricsData);

      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };

    fetchPortfolioData();
  }, []);

  if (loading) return <p>Loading portfolio data...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div id="portfolio-values-section" className="content-section">
      <h2>Portfolio Values</h2>
      <div id="metrics-display">
        <h3>Advanced Metrics</h3>
        <p>Sharpe Ratio: {advancedMetrics.sharpe_ratio}</p>
        <p>Sortino Ratio: {advancedMetrics.sortino_ratio}</p>
        <p>Beta: {advancedMetrics.beta}</p>
        <p>Alpha: {advancedMetrics.alpha}</p>
      </div>
      <h3>Daily Portfolio Values</h3>
      <table id="portfolio_value_table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Current Value</th>
            <th>Cost</th>
            <th>Current P&L</th>
            <th>Closed P&L</th>
            <th>Overall P&L</th>
            <th>Net Invested Capital</th>
            <th>Cumulative Cash Flow Adjusted Return</th>
            <th>Drawdown</th>
          </tr>
        </thead>
        <tbody>
          {portfolioValues.map((row, index) => (
            <tr key={index}>
              <td>{row.Date}</td>
              <td>{row['Current Value']}</td>
              <td>{row.Cost}</td>
              <td>{row['Current P&L']}</td>
              <td>{row['Closed P&L']}</td>
              <td>{row['Overall P&L']}</td>
              <td>{row['Net Invested Capital']}</td>
              <td>{(row['Cumulative Cash Flow Adjusted Return'] * 100).toFixed(2)}%</td>
              <td>{(row.Drawdown * 100).toFixed(2)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PortfolioValuesSection;