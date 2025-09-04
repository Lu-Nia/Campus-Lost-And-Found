import React from 'react';
import ItemCard from './ItemCard';
import '../styles/ItemList.css';

const ItemList = ({ items, loading, onStatusUpdate, onItemDelete }) => {
  if (loading) {
    return <div className="loading">Loading items...</div>;
  }

  if (items.length === 0) {
    return <div className="no-items">No items found matching your filters.</div>;
  }

  return (
    <div className="item-list">
      {items.map(item => (
        <ItemCard 
          key={item.id} 
          item={item} 
          onStatusUpdate={onStatusUpdate}
          onItemDelete={onItemDelete}
        />
      ))}
    </div>
  );
};

export default ItemList;