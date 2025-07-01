import React, { useState, useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

function ChartsSection() {
  const [activeTab, setActiveTab] = useState('portfolio-value-chart-tab');
  const [chartData, setChartData] = useState({
    portfolioValue: { dates: [], current_value: [], cost: [] },
    dailyPnl: { dates: [], daily_pnl_change: [] },
    assetAllocation: { labels: [], values: [] },
    twrVsSpy: { dates: [], portfolio_twr: [], spy_twr: [] },
    cumulativeReturn: { dates: [], cumulative_return: [] },
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const chartRefs = {
    portfolioValue: useRef(null),
    dailyPnl: useRef(null),
    assetAllocation: useRef(null),
    twrVsSpy: useRef(null),
    cumulativeReturn: useRef(null),
  };

  const chartInstances = useRef({});

  const fetchData = async () => {
    try {
      const [pvRes, dpRes, aaRes, twrRes, crRes] = await Promise.all([
        fetch('/data/chart/portfolio_value_over_time'),
        fetch('/data/chart/daily_pnl_change'),
        fetch('/data/chart/asset_allocation'),
        fetch('/data/chart/twr_vs_spy'),
        fetch('/data/chart/cumulative_cash_flow_adjusted_return'),
      ]);

      const [pvData, dpData, aaData, twrData, crData] = await Promise.all([
        pvRes.json(),
        dpRes.json(),
        aaRes.json(),
        twrRes.json(),
        crRes.json(),
      ]);

      setChartData({
        portfolioValue: pvData,
        dailyPnl: dpData,
        assetAllocation: aaData,
        twrVsSpy: twrData,
        cumulativeReturn: crData,
      });
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (!loading && !error) {
      // Destroy existing chart instances before re-rendering
      Object.values(chartInstances.current).forEach(chart => {
        if (chart) chart.destroy();
      });
      chartInstances.current = {}; // Clear the ref

      // Render charts based on activeTab
      if (activeTab === 'portfolio-value-chart-tab') {
        renderPortfolioValueChart();
      } else if (activeTab === 'daily-pnl-chart-tab') {
        renderDailyPnlChart();
      } else if (activeTab === 'asset-allocation-chart-tab') {
        renderAssetAllocationChart();
      } else if (activeTab === 'twr-chart-tab') {
        renderTwrVsSpyChart();
      } else if (activeTab === 'cumulative-return-chart-tab') {
        renderCumulativeReturnChart();
      }
    }
  }, [loading, error, activeTab, chartData]); // Re-render when data or activeTab changes

  const renderPortfolioValueChart = () => {
    if (chartRefs.portfolioValue.current) {
      const ctx = chartRefs.portfolioValue.current.getContext('2d');
      chartInstances.current.portfolioValue = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.portfolioValue.dates,
          datasets: [
            {
              label: 'Total Portfolio Value',
              data: chartData.portfolioValue.current_value,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
            },
            {
              label: 'Total Cost',
              data: chartData.portfolioValue.cost,
              borderColor: 'rgb(255, 99, 132)',
              tension: 0.1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    }
  };

  const renderDailyPnlChart = () => {
    if (chartRefs.dailyPnl.current) {
      const ctx = chartRefs.dailyPnl.current.getContext('2d');
      chartInstances.current.dailyPnl = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: chartData.dailyPnl.dates,
          datasets: [
            {
              label: 'Daily P&L Change',
              data: chartData.dailyPnl.daily_pnl_change,
              backgroundColor: chartData.dailyPnl.daily_pnl_change.map(pnl => pnl > 0 ? 'rgba(75, 192, 192, 0.6)' : 'rgba(255, 99, 132, 0.6)'),
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    }
  };

  const renderAssetAllocationChart = () => {
    if (chartRefs.assetAllocation.current) {
      const ctx = chartRefs.assetAllocation.current.getContext('2d');
      chartInstances.current.assetAllocation = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: chartData.assetAllocation.labels,
          datasets: [
            {
              data: chartData.assetAllocation.values,
              backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)',
              ],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    }
  };

  const renderTwrVsSpyChart = () => {
    if (chartRefs.twrVsSpy.current) {
      const ctx = chartRefs.twrVsSpy.current.getContext('2d');
      chartInstances.current.twrVsSpy = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.twrVsSpy.dates,
          datasets: [
            {
              label: 'Portfolio TWR',
              data: chartData.twrVsSpy.portfolio_twr,
              borderColor: 'rgb(255, 99, 132)',
              tension: 0.1,
            },
            {
              label: 'SPY TWR',
              data: chartData.twrVsSpy.spy_twr,
              borderColor: 'rgb(54, 162, 235)',
              tension: 0.1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    }
  };

  const renderCumulativeReturnChart = () => {
    if (chartRefs.cumulativeReturn.current) {
      const ctx = chartRefs.cumulativeReturn.current.getContext('2d');
      chartInstances.current.cumulativeReturn = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.cumulativeReturn.dates,
          datasets: [
            {
              label: 'Cumulative Cash Flow Adjusted Return',
              data: chartData.cumulativeReturn.cumulative_return.map(val => val * 100), // Convert to percentage
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
        },
      });
    }
  };

  if (loading) return <p>Loading charts...</p>;
  if (error) return <p>Error loading charts: {error.message}</p>;

  return (
    <div id="charts-section" className="content-section">
      <h2>Charts</h2>
      <div className="tabs">
        <button
          className={`chart-tab-button ${activeTab === 'portfolio-value-chart-tab' ? 'active' : ''}`}
          onClick={() => setActiveTab('portfolio-value-chart-tab')}
        >
          Portfolio Value
        </button>
        <button
          className={`chart-tab-button ${activeTab === 'daily-pnl-chart-tab' ? 'active' : ''}`}
          onClick={() => setActiveTab('daily-pnl-chart-tab')}
        >
          Daily P&L
        </button>
        <button
          className={`chart-tab-button ${activeTab === 'asset-allocation-chart-tab' ? 'active' : ''}`}
          onClick={() => setActiveTab('asset-allocation-chart-tab')}
        >
          Asset Allocation
        </button>
        <button
          className={`chart-tab-button ${activeTab === 'twr-chart-tab' ? 'active' : ''}`}
          onClick={() => setActiveTab('twr-chart-tab')}
        >
          TWR vs SPY
        </button>
        <button
          className={`chart-tab-button ${activeTab === 'cumulative-return-chart-tab' ? 'active' : ''}`}
          onClick={() => setActiveTab('cumulative-return-chart-tab')}
        >
          Cumulative Return
        </button>
      </div>

      <div id="portfolio-value-chart-tab" className={`chart-tab-content ${activeTab === 'portfolio-value-chart-tab' ? 'active' : ''}`}>
        <h3>Portfolio Value Over Time</h3>
        <canvas ref={chartRefs.portfolioValue}></canvas>
      </div>
      <div id="daily-pnl-chart-tab" className={`chart-tab-content ${activeTab === 'daily-pnl-chart-tab' ? 'active' : ''}`}>
        <h3>Daily P&L Change</h3>
        <canvas ref={chartRefs.dailyPnl}></canvas>
      </div>
      <div id="asset-allocation-chart-tab" className={`chart-tab-content ${activeTab === 'asset-allocation-chart-tab' ? 'active' : ''}`}>
        <h3>Asset Allocation</h3>
        <canvas ref={chartRefs.assetAllocation}></canvas>
      </div>
      <div id="twr-chart-tab" className={`chart-tab-content ${activeTab === 'twr-chart-tab' ? 'active' : ''}`}>
        <h3>Time-Weighted Return (TWR) vs. SPY</h3>
        <canvas ref={chartRefs.twrVsSpy}></canvas>
      </div>
      <div id="cumulative-return-chart-tab" className={`chart-tab-content ${activeTab === 'cumulative-return-chart-tab' ? 'active' : ''}`}>
        <h3>Cumulative Cash Flow Adjusted Return</h3>
        <canvas ref={chartRefs.cumulativeReturn}></canvas>
      </div>
    </div>
  );
}

export default ChartsSection;