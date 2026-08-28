/* ===== 消息渲染器 ===== */
const ChatRenderer = {
  chatArea: null,
  chartInstances: {},
  factInterval: null,

  /** 电脑冷知识/小技巧（等待时展示） */
  funFacts: [
    "CPU 的 \"i5\" 不是第5代，而是中端定位的意思",
    "笔记本的 85Wh 电池大约可以给手机充 5 次电",
    "RTX 4060 比 RTX 3060 性能提升约 20%，但功耗更低",
    "机械键盘的轴体寿命通常可达 5000 万次敲击",
    "M.2 NVMe 固态硬盘速度是 SATA SSD 的 5-7 倍",
    "笔记本长期插电使用，建议将电池充电上限设为 80%",
    "DDR5 内存比 DDR4 速度快约 50%，但延迟略高",
    "Intel 第13/14代酷睿桌面CPU存在电压不稳问题，已通过微码修复",
    "OLED 屏幕对比度是 IPS 的 100 倍，但有烧屏风险",
    "笔记本清灰换硅脂每年做一次，可降低 5-10°C",
    "AMD 的 3D V-Cache 技术可以让游戏性能提升 15%",
    "苹果 M4 芯片的单核性能已超越所有 x86 桌面处理器",
    "雷电 5 接口速率达 80Gbps，是 USB4 的两倍",
    "笔记本外接显示器时，独显直连模式性能更好",
    "2025 年 Wi-Fi 7 开始普及，速度是 Wi-Fi 6 的 4 倍",
    "同配置下，游戏本比轻薄本性能强 30-50%",
    "选择笔记本时，GPU 性能比 CPU 更影响游戏体验",
    "台式机同价位性能通常是笔记本的 1.5-2 倍",
    "5000 元台式机可以畅玩 2K 分辨率 3A 大作",
    "3nm 制程相比 5nm 功耗降低约 30%",
    "笔记本散热支架可以降低 3-8°C 的温度",
    "AMD 的 FSR 和 NVIDIA 的 DLSS 都能大幅提升游戏帧率",
    "笔记本内存是焊死还是插槽，直接影响未来升级空间",
    "屏幕色域: sRGB < DCI-P3 < AdobeRGB，P3 是目前主流",
    "Type-C 充电是目前笔记本轻薄化的重要推动力",
    "笔记本的\"性能模式\"会显著增加风扇噪音和温度",
    "Wi-Fi 7 理论速度可达 46Gbps，是 Wi-Fi 6 的 4 倍",
    "Apple Silicon 的统一内存架构使其在AI任务中效率极高",
  ],

  init(chatArea) {
    this.chatArea = chatArea;
  },

  /** 添加加载状态消息（带电脑冷知识轮播） */
  addStatus(text) {
    this.removeStatus();
    const fact = this.funFacts[Math.floor(Math.random() * this.funFacts.length)];
    const div = document.createElement('div');
    div.className = 'message status-msg';
    div.id = 'statusMsg';
    div.innerHTML = `<div class="avatar">⏳</div>
      <div class="bubble">
        <div class="status-text"><span>${text}</span> <span class="typing-dots"><span></span><span></span><span></span></span></div>
        <div class="status-fact" id="statusFact">💡 ${fact}</div>
      </div>`;
    this.chatArea.appendChild(div);

    this.factInterval = setInterval(() => {
      const el = document.getElementById('statusFact');
      if (el) {
        const f = this.funFacts[Math.floor(Math.random() * this.funFacts.length)];
        el.textContent = '💡 ' + f;
      }
    }, 5000);

    this.scrollToBottom();
  },

  /** 更新状态文字（保留冷知识） */
  updateStatus(text) {
    const el = document.getElementById('statusMsg');
    if (el) {
      const factEl = el.querySelector('.status-fact');
      const factText = factEl ? factEl.textContent : '';
      el.querySelector('.bubble').innerHTML =
        `<div class="status-text"><span>${text}</span> <span class="typing-dots"><span></span><span></span><span></span></span></div>
         <div class="status-fact">${factText}</div>`;
      this.scrollToBottom();
    }
  },

  /** 移除状态消息（清理定时器） */
  removeStatus() {
    if (this.factInterval) {
      clearInterval(this.factInterval);
      this.factInterval = null;
    }
    const el = document.getElementById('statusMsg');
    if (el) el.remove();
  },

  /** 添加用户消息 */
  addUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'message user';
    div.innerHTML = `<div class="avatar">🙂</div><div class="bubble">${Utils.escapeHtml(text)}</div>`;
    this.chatArea.appendChild(div);
    this.scrollToBottom();
  },

  /** 添加追问消息 */
  addClarify(question, options) {
    const div = document.createElement('div');
    div.className = 'message assistant';
    const hasOptions = options && options.length;
    const optsHtml = hasOptions
      ? `<div class="clarify-options">${options.map(opt =>
          `<button class="clarify-btn" data-text="${Utils.escapeHtml(opt)}">${Utils.escapeHtml(opt)}</button>`
        ).join('')}</div>`
      : '';
    div.innerHTML = `<div class="avatar">🤖</div><div class="bubble">${Utils.escapeHtml(question)}${optsHtml}</div>`;
    this.chatArea.appendChild(div);

    if (hasOptions) {
      div.querySelectorAll('.clarify-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          document.getElementById('messageInput').value = btn.dataset.text;
          document.getElementById('sendBtn').click();
        });
      });
    }
    this.scrollToBottom();
  },

  /** 添加推荐结果（核心渲染） */
  addRecommendation(data) {
    // 清理旧图表实例
    Object.values(this.chartInstances).forEach(c => { try { c.destroy(); } catch(e) {} });
    this.chartInstances = {};

    const div = document.createElement('div');
    div.className = 'message assistant';
    const products = data.products || [];
    const charts = data.charts || {};
    const followups = data.followup_hints || [];

    let html = `<div class="avatar">🤖</div><div class="bubble">`;

    // 1. 摘要文字
    if (data.summary) {
      html += `<div class="recommendation-summary">${data.summary.replace(/\n/g, '<br>')}</div>`;
    }

    // 1.5 数据来源说明
    const totalReviews = products.reduce((sum, p) => sum + ((p.score_breakdown && p.score_breakdown.items) ? p.score_breakdown.items.length : 0), 0);
    html += `<div class="data-source-info">
      数据来源：聚合 ${totalReviews} 条评测数据（视频评测优先加权）
      <span class="source-detail-toggle" onclick="const n=this.nextElementSibling;n.style.display=n.style.display==='none'?'block':'none'">评分规则</span>
      <div class="source-detail-content" style="display:none">
        <div>📹 视频评测(50%) > 📝 图文评测(30%) > 💬 论坛(10%) > 🛒 电商(10%)</div>
        <div>不直接采用电商评分，基于评测原文由 AI 分析提取</div>
      </div>
    </div>`;

    // 2. 排序表格
    if (products.length) {
      html += `<div class="product-table-wrapper"><table class="product-table">
        <thead><tr><th>#</th><th>产品</th><th>价格</th><th>评分</th><th>配置</th><th>来源</th></tr></thead><tbody>`;
      products.forEach((p, i) => {
        html += `<tr>
          <td>${Utils.getRankBadge(i + 1)}</td>
          <td><strong>${Utils.escapeHtml(p.name)}</strong><br><span class="match-tag">${Utils.escapeHtml(p.match)}</span></td>
          <td class="price-cell">${p.price}${p.original_price ? `<span class="origin-price">${p.original_price}</span>` : ''}</td>
          <td class="score-cell">${p.rating}</td>
          <td class="config-cell">${Utils.escapeHtml(p.config || '')}</td>
          <td>${p.source ? `<span class="source-tag">${Utils.escapeHtml(p.source)}</span>` : ''}</td>
        </tr>`;
      });
      html += `</tbody></table></div>`;
    }

    // 3. 图表
    const chartId = 'charts-' + Date.now();
    if (charts.radar || charts.price_bar) {
      html += `<div class="charts-container" id="${chartId}">`;
      if (charts.radar) {
        html += `<div class="chart-box"><h4>评分雷达对比</h4>
          <div class="chart-canvas-wrapper"><canvas id="radar-${chartId}"></canvas></div></div>`;
      }
      if (charts.price_bar) {
        html += `<div class="chart-box"><h4>价格对比（元）</h4>
          <div class="chart-canvas-wrapper"><canvas id="price-${chartId}"></canvas></div></div>`;
      }
      html += `</div>`;
    }

    // 4. 产品卡片
    if (products.length) {
      html += `<div class="product-cards">`;
      products.forEach((p, i) => {
        const medal = ['🥇', '🥈', '🥉'][i] || `${i + 1}.`;
        html += `<div class="product-card">
          <div class="card-header">
            <span class="card-rank">${medal}</span>
            <span class="card-title">${Utils.escapeHtml(p.name)}</span>
            <span class="card-price">${p.price}</span>
          </div>
          <div class="card-body">
            <div class="card-config">${Utils.escapeHtml(p.config || '暂无配置')}</div>
            <div class="card-details">
              <div class="card-pros"><h5>优点</h5><ul>${
                (p.pros || []).map(x => `<li>${Utils.escapeHtml(x)}</li>`).join('')
              }</ul></div>
              <div class="card-cons"><h5>缺点</h5><ul>${
                (p.cons || []).map(x => `<li>${Utils.escapeHtml(x)}</li>`).join('')
              }</ul></div>
            </div>
          </div>
          <div class="card-score">
            <span>${Utils.escapeHtml(p.match)}</span>
            <span>综合 <strong>${p.rating}</strong></span>
          </div>
          ${p.score_breakdown && p.score_breakdown.items ? this.renderScoreBreakdown(p) : ''}
        </div>`;
      });
      html += `</div>`;
    }

    // 5. 追问引导
    if (followups.length) {
      html += `<div class="followup-hints">`;
      followups.forEach(h => {
        html += `<button class="followup-btn" data-text="${Utils.escapeHtml(h)}">${Utils.escapeHtml(h)}</button>`;
      });
      html += `</div>`;
    }

    html += `</div></div>`;
    div.innerHTML = html;
    this.chatArea.appendChild(div);

    // 绑定追问按钮
    div.querySelectorAll('.followup-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.getElementById('messageInput').value = btn.dataset.text;
        document.getElementById('sendBtn').click();
      });
    });

    // 延迟渲染图表（等 DOM 渲染完成）
    setTimeout(() => {
      if (charts.radar && document.getElementById('radar-' + chartId)) {
        this.renderRadar(charts.radar, 'radar-' + chartId);
      }
      if (charts.price_bar && document.getElementById('price-' + chartId)) {
        this.renderPriceBar(charts.price_bar, 'price-' + chartId);
      }
    }, 50);

    this.scrollToBottom();
  },

  /** 渲染雷达图 */
  renderRadar(data, canvasId) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    const colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6'];
    const datasets = (data.datasets || []).map((ds, i) => ({
      label: ds.label,
      data: ds.data,
      borderColor: colors[i % colors.length],
      backgroundColor: colors[i % colors.length] + '25',
      borderWidth: 2,
      pointRadius: 3,
      pointBackgroundColor: colors[i % colors.length],
    }));
    try {
      this.chartInstances[canvasId] = new Chart(ctx, {
        type: 'radar',
        data: { labels: data.labels || [], datasets },
        options: {
          responsive: true, maintainAspectRatio: false,
          scales: {
            r: { beginAtZero: true, max: 10, ticks: { stepSize: 2, font: { size: 10 } },
              pointLabels: { font: { size: 11 } } }
          },
          plugins: {
            legend: { position: 'bottom', labels: { font: { size: 10 }, boxWidth: 12, padding: 10 } }
          }
        }
      });
    } catch(e) { console.warn('雷达图渲染失败:', e); }
  },

  /** 渲染价格柱状图 */
  renderPriceBar(data, canvasId) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    try {
      this.chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels || [],
          datasets: (data.datasets || []).map(ds => ({
            label: ds.label || '价格',
            data: ds.data,
            backgroundColor: ds.backgroundColor || ['#10B981', '#34D399', '#6EE7B7', '#A7F3D0', '#D1FAE5'],
            borderRadius: 4,
          }))
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {
            x: { beginAtZero: true, ticks: { callback: v => '¥' + Number(v).toLocaleString(), font: { size: 10 } } },
            y: { ticks: { font: { size: 10 } } }
          },
          plugins: {
            legend: { display: false },
            tooltip: { callbacks: { label: ctx => '¥' + Number(ctx.raw).toLocaleString() } }
          }
        }
      });
    } catch(e) { console.warn('价格图渲染失败:', e); }
  },

  /** 渲染评分明细（打分卡） */
  renderScoreBreakdown(product) {
    const sb = product.score_breakdown;
    if (!sb || !sb.items || !sb.items.length) return '';

    let html = `<div class="score-breakdown">
      <div class="score-toggle" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none';this.querySelector('.arrow').textContent=this.querySelector('.arrow').textContent==='▶'?'▼':'▶'">
        <span class="arrow">▶</span> 查看评分明细 · 综合 ${product.rating}
      </div>
      <div class="score-detail" style="display:none">
        <div class="score-base">${Utils.escapeHtml(sb.base || '')}</div>
        <div class="score-items">`;
    sb.items.forEach(item => {
      const impact = (item.impact || '0').trim() || '0';
      const sign = parseFloat(impact) >= 0 ? '+' : '';
      const cls = parseFloat(impact) >= 0 ? 'score-positive' : 'score-negative';
      const typeIcon = item.type === 'video' ? '📹' : (item.type === 'ecommerce' ? '🛒' : '📝');
      html += `<div class="score-item ${cls}">
        <span class="score-source">${typeIcon} ${Utils.escapeHtml(item.source || '')}</span>
        <span class="score-content">${Utils.escapeHtml(item.content || '')}</span>
        <span class="score-impact">${sign}${impact}</span>
      </div>`;
    });
    html += `</div>
        <div class="score-total">${Utils.escapeHtml(sb.formula || '')}</div>
        <div class="score-note">* 评分基于多源评测数据聚合，不依赖电商评分</div>
      </div>
    </div>`;
    return html;
  },

  /** 添加错误消息 */
  addError(text) {
    this.removeStatus();
    const div = document.createElement('div');
    div.className = 'message error-msg';
    div.innerHTML = `<div class="avatar">⚠️</div><div class="bubble">${Utils.escapeHtml(text)}</div>`;
    this.chatArea.appendChild(div);
    this.scrollToBottom();
  },

  /** 清空对话（保留欢迎消息） */
  clear() {
    Object.values(this.chartInstances).forEach(c => { try { c.destroy(); } catch(e) {} });
    this.chartInstances = {};
    this.chatArea.querySelectorAll('.message:not(.welcome-msg)').forEach(el => el.remove());
  },

  scrollToBottom() {
    requestAnimationFrame(() => {
      this.chatArea.scrollTop = this.chatArea.scrollHeight;
    });
  }
};

