import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import '../styles/ItemCard.css';

const ItemCard = ({ item, onStatusUpdate, onItemDelete }) => {
  const { currentUser } = useAuth();
  const [updating, setUpdating] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [showClaimConfirm, setShowClaimConfirm] = useState(false);

  const isOwner = currentUser.id === item.user_id;

  const handleStatusUpdate = async (newStatus) => {
    if (isOwner) return;
    
    setUpdating(true);
    try {
      await axios.patch(`http://localhost:8000/items/${item.id}`, {
        status: newStatus
      });
      onStatusUpdate();
    } catch (error) {
      console.error('Error updating status:', error);
      alert('Failed to update status');
    } finally {
      setUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!isOwner) return;
    
    if (!window.confirm('Are you sure you want to delete this item?')) return;
    
    setDeleting(true);
    try {
      // If status is found, update to claimed first
      if (item.status === 'found') {
        await axios.patch(`http://localhost:8000/items/${item.id}`, {
          status: 'claimed'
        });
      }
      
      await axios.delete(`http://localhost:8000/items/${item.id}`);
      onItemDelete();
    } catch (error) {
      console.error('Error deleting item:', error);
      alert(error.response?.data?.detail || 'Failed to delete item');
    } finally {
      setDeleting(false);
    }
  };

  const handleClaim = async () => {
    if (!window.confirm('Are you sure you want to claim this item?')) return;
    
    setUpdating(true);
    try {
      await axios.patch(`http://localhost:8000/items/${item.id}`, {
        status: 'claimed'
      });
      
      // Show confirmation message
      setShowClaimConfirm(true);
      
      // After 5 seconds, refresh the item list to reflect the new status
      setTimeout(() => {
        onStatusUpdate(); // This should refresh the parent component's item list
        setShowClaimConfirm(false); // Hide the confirmation message
      }, 5000);
    } catch (error) {
      console.error('Error claiming item:', error);
      alert('Failed to claim item');
    } finally {
      setUpdating(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'lost': return '#dc3545';
      case 'found': return '#28a745';
      case 'claimed': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const canUpdateStatus = !isOwner && item.status !== 'claimed';
  const canDelete = isOwner && (item.status === 'found' || item.status === 'claimed');
  const showClaimButton = !isOwner && item.status === 'found';

  if (showClaimConfirm) {
    return (
      <div className="item-card claimed-confirmation">
        <h3>Item Claimed Successfully!</h3>
        <p>This item has been marked as claimed.</p>
        <p>The list will refresh in 5 seconds...</p>
      </div>
    );
  }

  return (
    <div className="item-card">
      {item.image_url && (
        <img 
          src={`http://localhost:8000${item.image_url}`} 
          alt={item.title}
          className="item-image"
        />
      )}
      
      <div className="item-content">
        <div className="item-header">
          <h3 className="item-title">{item.title}</h3>
          <span 
            className="item-status"
            style={{ backgroundColor: getStatusColor(item.status) }}
          >
            {item.status.toUpperCase()}
          </span>
        </div>
        
        <p className="item-description">{item.description}</p>
        
        <div className="item-details">
          <div className="item-detail">
            <strong>Category:</strong> {item.category}
          </div>
          <div className="item-detail">
            <strong>Location:</strong> {item.location || 'Not specified'}
          </div>
          <div className="item-detail">
            <strong>Contact:</strong> 
            <a href={`tel:${item.contact_phone}`} className="contact-link">
              {item.contact_phone}
            </a>
          </div>
          <div className="item-detail">
            <strong>Reported by:</strong> {item.owner_name || 'Unknown'}
          </div>
          
          <div className="item-detail">
            <strong>Reported:</strong> {new Date(item.created_at).toLocaleDateString()}
          </div>
        </div>

        <div className="item-actions">
          {canUpdateStatus && item.status === 'lost' && (
            <button
              onClick={() => handleStatusUpdate('found')}
              disabled={updating}
              className="status-btn found-btn"
            >
              {updating ? 'Updating...' : 'Mark as Found'}
            </button>
          )}
          
          {showClaimButton && (
            <button
              onClick={handleClaim}
              disabled={updating}
              className="status-btn claim-btn"
            >
              {updating ? 'Claiming...' : 'Claim Item'}
            </button>
          )}
          
          {canDelete && (
            <button
              onClick={handleDelete}
              disabled={deleting}
              className="delete-btn"
            >
              {deleting ? 'Deleting...' : 'Delete'}
            </button>
          )}
        </div>

        {isOwner && item.status === 'lost' && (
          <div className="owner-notice">
            <p>You reported this item. Others can help mark it as found.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ItemCard;