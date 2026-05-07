import React from 'react';
import ReactDOM from 'react-dom/client';

function Popup() {
  return (
    <div style={{padding: '16px', minWidth: '280px'}}>
      <h2>EduSense</h2>
      <p>Privacy-first learning intelligence</p>
      <p style={{color:'green'}}>● Active</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('app')!).render(<Popup />);
