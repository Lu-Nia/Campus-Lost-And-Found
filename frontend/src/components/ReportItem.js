import React, { useState } from 'react';
import axios from 'axios';
import '../styles/ReportItem.css';

const ReportItem = ({ onCancel, onSuccess }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: '',
    location: '',
    contact_phone: '',
    image: null
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const categories = ['Accessories', 'Cards', 'Clothing', 'Electronics', 'Others'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleImageChange = (e) => {
    setFormData(prev => ({ ...prev, image: e.target.files[0] }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const formDataToSend = new FormData();
      formDataToSend.append('title', formData.title);
      formDataToSend.append('description', formData.description);
      formDataToSend.append('category', formData.category);
      formDataToSend.append('location', formData.location);
      formDataToSend.append('contact_phone', formData.contact_phone);
      
      if (formData.image) {
        formDataToSend.append('image', formData.image);
      }

      console.log('Sending form data:', Object.fromEntries(formDataToSend));

      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await axios.post('http://localhost:8000/items', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${token}`
        }
      });

      console.log('Response:', response.data);
      onSuccess();
    } catch (error) {
      console.error('Full error:', error);
      console.error('Error response:', error.response);
      
      let errorMessage = 'Failed to create item';
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="report-item-form">
      <h2>Report Found Item</h2>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Item Title *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="category">Category *</label>
          <select
            id="category"
            name="category"
            value={formData.category}
            onChange={handleChange}
            required
          >
            <option value="">Select a category</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="location">Location Found</label>
          <input
            type="text"
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
            placeholder="Where did you find this item?"
          />
        </div>

        <div className="form-group">
          <label htmlFor="contact_phone">Contact Phone Number</label>
          <input
            type="tel"
            id="contact_phone"
            name="contact_phone"
            value={formData.contact_phone}
            onChange={handleChange}
            placeholder="Phone number for people to contact you"
          />
        </div>

        <div className="form-group">
          <label htmlFor="image">Item Image</label>
          <input
            type="file"
            id="image"
            name="image"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>

        <div className="form-actions">
          <button 
            type="button" 
            onClick={onCancel}
            className="cancel-btn"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            disabled={loading}
            className="submit-btn"
          >
            {loading ? 'Reporting...' : 'Report Item'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReportItem;