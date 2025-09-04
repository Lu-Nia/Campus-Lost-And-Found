import React, { useState } from 'react';
import '../styles/FilterBar.css';

const FilterBar = ({ onFilterChange }) => {
  const [filters, setFilters] = useState({
    category: '',
    status: '',
    location: '',
    search: ''
  });

  const categories = ['Accessories', 'Cards', 'Clothing', 'Electronics', 'Others'];
  const statuses = ['lost', 'found', 'claimed'];

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearFilters = () => {
    const emptyFilters = {
      category: '',
      status: '',
      location: '',
      search: ''
    };
    setFilters(emptyFilters);
    onFilterChange(emptyFilters);
  };

  return (
    <div className="filter-bar">
      <h3>Filters</h3>
      
      <div className="filter-group">
        <label>Search</label>
        <input
          type="text"
          placeholder="Search items..."
          value={filters.search}
          onChange={(e) => handleFilterChange('search', e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label>Category</label>
        <select
          value={filters.category}
          onChange={(e) => handleFilterChange('category', e.target.value)}
        >
          <option value="">All Categories</option>
          {categories.map(category => (
            <option key={category} value={category}>{category}</option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label>Status</label>
        <select
          value={filters.status}
          onChange={(e) => handleFilterChange('status', e.target.value)}
        >
          <option value="">All Statuses</option>
          {statuses.map(status => (
            <option key={status} value={status}>{status.charAt(0).toUpperCase() + status.slice(1)}</option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label>Location</label>
        <input
          type="text"
          placeholder="Enter location..."
          value={filters.location}
          onChange={(e) => handleFilterChange('location', e.target.value)}
        />
      </div>

      <button className="clear-filters-btn" onClick={clearFilters}>
        Clear Filters
      </button>
    </div>
  );
};

export default FilterBar;