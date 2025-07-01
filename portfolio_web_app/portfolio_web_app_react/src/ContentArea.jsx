import React from 'react';

function ContentArea() {
  return (
    <div className="content-area">
      <h1>My Portfolio Dashboard</h1>

      <div id="welcome-section" className="content-section">
        <h2>Welcome to Your Portfolio Tracker!</h2>
        <p>Use the navigation on the left to explore your portfolio's performance, view detailed positions, or add new transactions.</p>
        {/* <img src="/static/welcome.jpg" alt="Welcome Image" className="welcome-image"> */}
      </div>
    </div>
  );
}

export default ContentArea;