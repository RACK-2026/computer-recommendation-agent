/* ===== 应用入口 ===== */
const App = {
  ws: null,
  sessionId: null,
  isProcessing: false,
  reconnectAttempts: 0,
  maxReconnect: 3,
  connected: false,

  async init() {
    this.chatArea = document.getElementById('chatArea');
    this.input = document.getElementById('messageInput');
    this.sendBtn = document.getElementById('sendBtn');
    this.clearBtn = document.getElementById('clearBtn');

    ChatRenderer.init(this.chatArea);

    // 生成或恢复会话 ID
    this.sessionId = localStorage.getItem('sessionId') || Utils.uuid();
    localStorage.setItem('sessionId', this.sessionId);

    this.bindEvents();
    await this.connect();
  },

  bindEvents() {
    this.sendBtn.addEventListener('click', () => this.sendMessage());
    this.input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
    this.clearBtn.addEventListener('click', () => {
      ChatRenderer.clear();
      this.sessionId = Utils.uuid();
      localStorage.setItem('sessionId', this.sessionId);
    });
    document.querySelectorAll('.quick-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.input.value = btn.dataset.msg;
        this.sendMessage();
      });
    });
  },

  async connect() {
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${location.host}/ws/chat`;

    try {
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('[WS] 已连接');
        this.reconnectAttempts = 0;
        this.connected = true;
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.handleServerMessage(data);
        } catch (e) {
          console.error('[WS] 解析消息失败:', e);
        }
      };

      this.ws.onclose = () => {
        console.log('[WS] 已断开');
        this.connected = false;
        this.isProcessing = false;
        this.sendBtn.disabled = false;
        ChatRenderer.removeStatus();
        if (this.reconnectAttempts < this.maxReconnect) {
          this.reconnectAttempts++;
          setTimeout(() => this.connect(), 2000);
        }
      };

      this.ws.onerror = () => {
        console.error('[WS] 连接错误');
      };

    } catch (err) {
      ChatRenderer.addError('⚠️ 无法连接到服务器，请确认服务已启动');
    }
  },

  async sendMessage() {
    const text = this.input.value.trim();
    if (!text || this.isProcessing || !this.connected) return;

    this.input.value = '';
    this.isProcessing = true;
    this.sendBtn.disabled = true;

    // 显示用户消息
    ChatRenderer.addUserMessage(text);
    // 显示加载状态
    ChatRenderer.addStatus('🤔 分析需求中...');

    try {
      this.ws.send(JSON.stringify({
        type: 'message',
        content: text,
        session_id: this.sessionId
      }));
    } catch (e) {
      ChatRenderer.removeStatus();
      ChatRenderer.addError('⚠️ 发送失败，连接已断开');
      this.isProcessing = false;
      this.sendBtn.disabled = false;
    }
  },

  handleServerMessage(data) {
    switch (data.type) {
      case 'connected':
        // 仅首次连接时更新 sessionId，不重置处理状态
        this.sessionId = data.session_id;
        localStorage.setItem('sessionId', this.sessionId);
        break;

      case 'status':
        ChatRenderer.updateStatus(data.content);
        break;

      case 'clarify':
        ChatRenderer.removeStatus();
        ChatRenderer.addClarify(data.content, data.options);
        this.isProcessing = false;
        this.sendBtn.disabled = false;
        break;

      case 'recommendation':
        ChatRenderer.removeStatus();
        ChatRenderer.addRecommendation(data);
        this.isProcessing = false;
        this.sendBtn.disabled = false;
        break;

      case 'error':
        ChatRenderer.removeStatus();
        ChatRenderer.addError(data.content);
        this.isProcessing = false;
        this.sendBtn.disabled = false;
        break;

      default:
        console.log('[WS] 未知消息类型:', data.type);
    }
  }
};

// 启动
document.addEventListener('DOMContentLoaded', () => App.init());

