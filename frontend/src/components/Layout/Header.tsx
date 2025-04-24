import React from 'react';
import { Link } from 'react-router';

const Header: React.FC = () => {
  return (
    <header className="app-header">
      <div className="logo">
        <Link to="/">Home Automation</Link>
      </div>
      <nav>
        <ul>
          <li><Link to="/">Dashboard</Link></li>
          <li><Link to="/devices">Devices</Link></li>
          <li><Link to="/settings">Settings</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;