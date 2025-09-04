import React from 'react';
import '../styles/StatsOverview.css';

const StatsOverview = ({ stats }) => {
  const statCards = [
    { title: 'Total Items', value: stats.total_items || 0, color: '#007bff' },
    { title: 'Lost Items', value: stats.lost_items || 0, color: '#dc3545' },
    { title: 'Found Items', value: stats.found_items || 0, color: '#28a745' },
    { title: 'Claimed Items', value: stats.claimed_items || 0, color: '#6c757d' }
  ];

  return (
    <div className="stats-overview">
      {statCards.map((stat, index) => (
        <div key={index} className="stat-card">
          <h3>{stat.title}</h3>
          <span style={{ color: stat.color }}>{stat.value}</span>
        </div>
      ))}
    </div>
  );
};

export default StatsOverview;