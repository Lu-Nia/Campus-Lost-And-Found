import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ItemList from '../components/ItemList';
import ReportItem from '../components/ReportItem';
import StatsOverview from '../components/StatsOverview';
import FilterBar from '../components/FilterBar';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState({});
  const [filters, setFilters] = useState({});
  const [showReportForm, setShowReportForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchItems();
    fetchStats();
  }, [filters]);

  const fetchItems = async () => {
    try {
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });

      const response = await axios.get(`http://localhost:8000/items?${params}`);
      setItems(response.data);
    } catch (error) {
      console.error('Error fetching items:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:8000/items/stats/overview');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const handleItemCreated = () => {
    setShowReportForm(false);
    fetchItems();
    fetchStats();
  };

  const handleStatusUpdate = () => {
    fetchItems();
    fetchStats();
  };

  const handleItemDelete = () => {
    fetchItems();
    fetchStats();
  };

  return (
    <div className="dashboard">
      <div className="dashboard-sidebar">
        <button 
          className="report-item-btn"
          onClick={() => setShowReportForm(true)}
        >
          Report Found Item
        </button>
        
        <FilterBar onFilterChange={handleFilterChange} />
      </div>

      <div className="dashboard-main">
        <StatsOverview stats={stats} />
        
        {showReportForm ? (
          <ReportItem 
            onCancel={() => setShowReportForm(false)}
            onSuccess={handleItemCreated}
          />
        ) : (
          <ItemList 
            items={items} 
            loading={loading}
            onStatusUpdate={handleStatusUpdate}
            onItemDelete={handleItemDelete}
          />
        )}
      </div>
    </div>
  );
};

export default Dashboard;