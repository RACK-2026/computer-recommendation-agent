/* ===== 工具函数 ===== */
const Utils = {
  /** 生成 UUID 短 ID */
  uuid() {
    return Math.random().toString(36).substring(2, 10);
  },

  /** 转义 HTML */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  /** 格式化价格 */
  formatPrice(price) {
    return `¥${Number(price).toLocaleString('zh-CN')}`;
  },

  /** 延迟 */
  sleep(ms) { return new Promise(r => setTimeout(r, ms)); },

  /** 获取排名徽章 */
  getRankBadge(rank) {
    if (rank === 1) return '<span class="rank-badge gold">🥇</span>';
    if (rank === 2) return '<span class="rank-badge silver">🥈</span>';
    if (rank === 3) return '<span class="rank-badge bronze">🥉</span>';
    return `<span class="rank-badge plain">${rank}</span>`;
  },

  /** 截断文本 */
  truncate(text, len = 30) {
    return text.length > len ? text.slice(0, len) + '...' : text;
  }
};

