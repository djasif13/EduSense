import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';

function Popup() {
  const [consented, setConsented] = useState<boolean | null>(null);

  useEffect(() => {
    chrome.storage.local.get(['consent_behavioral'], (r) => {
      setConsented(r.consent_behavioral ?? null);
    });
  }, []);

  const grant = () => {
    chrome.storage.local.set({ consent_behavioral: true });
    setConsented(true);
  };

  const revoke = () => {
    chrome.storage.local.set({ consent_behavioral: false });
    setConsented(false);
  };

  return (
    <div style={{ padding: '16px', minWidth: '280px', fontFamily: 'sans-serif' }}>
      <h2 style={{ fontSize: '16px', marginBottom: '8px' }}>EduSense</h2>
      <p style={{ fontSize: '12px', color: '#555', marginBottom: '12px' }}>
        Privacy-first learning intelligence. Only behavioral signals collected. No camera. No PII.
      </p>
      {consented === null && (
        <>
          <p style={{ fontSize: '13px', marginBottom: '8px' }}>Allow behavioral signal collection?</p>
          <button onClick={grant} style={{ marginRight: '8px', padding: '6px 12px', background: '#16a34a', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Allow</button>
          <button onClick={revoke} style={{ padding: '6px 12px', background: '#dc2626', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Deny</button>
        </>
      )}
      {consented === true && (
        <>
          <p style={{ color: '#16a34a', fontSize: '13px' }}>● Consent granted — signals active</p>
          <button onClick={revoke} style={{ marginTop: '8px', padding: '6px 12px', background: '#dc2626', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Revoke</button>
        </>
      )}
      {consented === false && (
        <>
          <p style={{ color: '#dc2626', fontSize: '13px' }}>● Consent denied — signals blocked</p>
          <button onClick={grant} style={{ marginTop: '8px', padding: '6px 12px', background: '#16a34a', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Allow</button>
        </>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('app')!).render(<Popup />);
