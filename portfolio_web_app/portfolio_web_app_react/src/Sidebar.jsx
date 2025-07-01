import React from 'react';
import { Link, useLocation } from 'react-router-dom';

function Sidebar() {
  const location = useLocation();

  return (
    <nav className="sidebar">
      <h2>Menu</h2>
      <ul>
        <li>
          <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
            <i className="fas fa-home"></i> Welcome
          </Link>
        </li>
        <li>
          <Link to="/charts" className={location.pathname === '/charts' ? 'active' : ''}>
            <i className="fas fa-chart-line"></i> Performance Charts
          </Link>
        </li>
        <li>
          <Link to="/portfolio-values" className={location.pathname === '/portfolio-values' ? 'active' : ''}>
            <i className="fas fa-wallet"></i> Portfolio Values
          </Link>
        </li>
        <li>
          <Link to="/open-positions" className={location.pathname === '/open-positions' ? 'active' : ''}>
            <i className="fas fa-folder-open"></i> Open Positions
          </Link>
        </li>
        <li>
          <Link to="/closed-positions" className={location.pathname === '/closed-positions' ? 'active' : ''}>
            <i className="fas fa-folder-closed"></i> Closed Positions
          </Link>
        </li>
        <li>
          <Link to="/add-transaction" className={location.pathname === '/add-transaction' ? 'active' : ''}>
            <i className="fas fa-plus-circle"></i> Add New Transaction
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Sidebar;