export default defineContentScript({
  matches: ['<all_urls>'],
  main() {
    const sessionId = crypto.randomUUID();
    const learnerId = 'anon-' + btoa(navigator.userAgent).slice(0, 12);
    const WS_URL = 'ws://localhost:8000/ws/ingest';
    let ws: WebSocket | null = null;

    function connect() {
      ws = new WebSocket(WS_URL);
      ws.onclose = () => setTimeout(connect, 3000);
    }
    connect();

    function send(state: string, signals: object) {
      if (ws?.readyState !== WebSocket.OPEN) return;
      ws.send(JSON.stringify({
        session_id: sessionId,
        learner_id: learnerId,
        consent_scope: ['behavioral'],
        learner_state: state,
        state_confidence: 0.7,
        timestamp: new Date().toISOString(),
        content_id: window.location.href,
        section_id: document.title,
        privacy_class: 'behavioral',
        signals
      }));
    }

    // Tab visibility
    document.addEventListener('visibilitychange', () => {
      send(document.hidden ? 'distracted' : 'focused', { tab_hidden: document.hidden });
    });

    // Idle detection
    let idleTimer: ReturnType<typeof setTimeout>;
    function resetIdle() {
      clearTimeout(idleTimer);
      idleTimer = setTimeout(() => send('idle', { idle: true }), 30000);
    }
    ['mousemove','keydown','scroll','click'].forEach(e => document.addEventListener(e, resetIdle));

    // Scroll depth
    document.addEventListener('scroll', () => {
      const depth = window.scrollY / (document.body.scrollHeight - window.innerHeight);
      send('engaged', { scroll_depth: Math.round(depth * 100) / 100 });
    }, { passive: true });

    console.log('[EduSense] Content script active');
  }
});
