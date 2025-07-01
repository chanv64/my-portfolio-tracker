import React, { useState } from 'react';

function AddTransactionSection() {
  const [formData, setFormData] = useState({
    date: '',
    ticker: '',
    type: 'Buy', // Default to Buy
    quantity: '',
    price: '',
    commission: '0',
  });
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState(''); // 'success' or 'error'

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('Submitting...');
    setMessageType('');

    const form = new FormData();
    for (const key in formData) {
      form.append(key, formData[key]);
    }

    try {
      const response = await fetch('/transactions', {
        method: 'POST',
        body: form,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message || 'Transaction added successfully!');
        setMessageType('success');
        // Optionally clear form after successful submission
        setFormData({
          date: '',
          ticker: '',
          type: 'Buy',
          quantity: '',
          price: '',
          commission: '0',
        });
      } else {
        setMessage(data.message || 'Error adding transaction.');
        setMessageType('error');
      }
    } catch (error) {
      setMessage(`Network error: ${error.message}`);
      setMessageType('error');
    }
  };

  return (
    <div id="add-transaction-section" className="content-section">
      <h2>Add New Transaction</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="date">Date:</label>
        <input type="date" id="date" name="date" value={formData.date} onChange={handleChange} required /><br /><br />

        <label htmlFor="ticker">Ticker:</label>
        <input type="text" id="ticker" name="ticker" value={formData.ticker} onChange={handleChange} required /><br /><br />

        <label htmlFor="type">Type:</label>
        <select id="type" name="type" value={formData.type} onChange={handleChange} required>
          <option value="Buy">Buy</option>
          <option value="Sell">Sell</option>
        </select><br /><br />

        <label htmlFor="quantity">Quantity:</label>
        <input type="number" id="quantity" name="quantity" value={formData.quantity} onChange={handleChange} required min="1" /><br /><br />

        <label htmlFor="price">Price:</label>
        <input type="number" step="0.01" id="price" name="price" value={formData.price} onChange={handleChange} required min="0.01" /><br /><br />

        <label htmlFor="commission">Commission:</label>
        <input type="number" step="0.01" id="commission" name="commission" value={formData.commission} onChange={handleChange} required min="0" /><br /><br />

        <button type="submit">Add Transaction</button>
      </form>
      {message && <p id="message" className={messageType}>{message}</p>}
    </div>
  );
}

export default AddTransactionSection;