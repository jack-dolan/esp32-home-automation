import React from 'react';
import { Link } from 'react-router';

const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar">
      <nav>
        <ul>
          <li><Link to="/">Dashboard</Link></li>
          <li><Link to="/devices">Devices</Link></li>
          <li><Link to="/settings">Settings</Link></li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;