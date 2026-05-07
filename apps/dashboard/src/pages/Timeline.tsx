import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Timeline: React.FC = () => {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/events?limit=20');
        setEvents(response.data);
      } catch (error) {
        console.error('Error fetching events:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 10000);

    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Loading...</div>;

  if (events.length === 0) return <div>No events yet</div>;

  return (
    <table className="w-full border-collapse">
      <thead>
        <tr>
          <th className="border px-4 py-2">Session ID</th>
          <th className="border px-4 py-2">Learner State</th>
          <th className="border px-4 py-2">State Confidence</th>
          <th className="border px-4 py-2">Timestamp</th>
        </tr>
      </thead>
      <tbody>
        {events.map((event, index) => (
          <tr key={index}>
            <td className="border px-4 py-2">{event.session_id}</td>
            <td className="border px-4 py-2">{event.learner_state}</td>
            <td className="border px-4 py-2">{event.state_confidence}</td>
            <td className="border px-4 py-2">{event.timestamp}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default Timeline;
