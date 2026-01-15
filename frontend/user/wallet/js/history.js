// ===============================
// Transaction History (Demo Only)
// ===============================

(function(window, document) {
  const STORAGE_KEY = 'transactions';
  let transactions = [];
  let currentPage = 1;
  const transactionsPerPage = 10;

  function loadTransactionHistory() {
    transactions = getStoredTransactions();
    currentPage = 1;

    if (transactions.length === 0) {
      showEmptyState();
      return;
    }

    renderSlice(transactions.slice(0, transactionsPerPage), true);
  }

  function addTransaction(transaction) {
    const normalized = {
      id: transaction.id || Date.now(),
      title: transaction.title,
      amount: Math.abs(transaction.amount),
      type: transaction.type, // 'credit' | 'debit'
      date: transaction.date ? new Date(transaction.date) : new Date(),
      status: transaction.status || 'completed'
    };

    transactions.unshift(normalized);
    persistTransactions();

    const visible = transactions.slice(0, currentPage * transactionsPerPage);
    renderSlice(visible, true);
  }

  function loadMoreTransactions() {
    currentPage += 1;
    const start = (currentPage - 1) * transactionsPerPage;
    const nextSlice = transactions.slice(start, start + transactionsPerPage);

    if (nextSlice.length === 0) {
      currentPage -= 1;
      return;
    }

    renderSlice(nextSlice, false);
  }

  function renderSlice(list, replaceContent) {
    const container = document.getElementById('transactionList');
    if (!container) return;

    if (replaceContent) {
      container.innerHTML = '';
    }

    if (list.length === 0 && replaceContent) {
      showEmptyState();
      return;
    }

    const fragment = document.createDocumentFragment();
    list.forEach(tx => {
      const item = document.createElement('div');
      item.className = 'transaction-item';

      item.innerHTML = `
        <div class="transaction-info">
          <div class="transaction-title">${tx.title}</div>
          <div class="transaction-date">${formatDate(tx.date)}</div>
        </div>
        <div class="transaction-amount ${tx.type}">
          ${tx.type === 'credit' ? '+' : '-'}${formatCurrency(tx.amount)}
        </div>
      `;

      fragment.appendChild(item);
    });

    container.appendChild(fragment);
  }

  function showEmptyState() {
    const container = document.getElementById('transactionList');
    if (!container) return;

    container.innerHTML = `
      <div class="empty-state">
        <p>Chưa có giao dịch nào</p>
        <p style="font-size:12px;margin-top:6px;">
          Nạp tiền hoặc thanh toán để xem lịch sử
        </p>
      </div>
    `;
  }

  function getStoredTransactions() {
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      return stored.map(item => ({
        id: item.id,
        title: item.title,
        amount: Math.abs(item.amount),
        type: item.type,
        date: item.date ? new Date(item.date) : new Date(),
        status: item.status || 'completed'
      }));
    } catch (error) {
      console.error('Không thể đọc lịch sử giao dịch:', error);
      return [];
    }
  }

  function persistTransactions() {
    const serializable = transactions.map(tx => ({
      id: tx.id,
      title: tx.title,
      amount: tx.amount,
      type: tx.type,
      date: tx.date instanceof Date ? tx.date.toISOString() : tx.date,
      status: tx.status
    }));

    localStorage.setItem(STORAGE_KEY, JSON.stringify(serializable));
  }

  function formatDate(date) {
    const d = date instanceof Date ? date : new Date(date);
    const now = new Date();

    const diffMs = now - d;
    const diffMin = Math.floor(diffMs / 60000);
    const diffHour = Math.floor(diffMin / 60);

    if (diffMin < 1) return 'Vừa xong';
    if (diffMin < 60) return `${diffMin} phút trước`;
    if (diffHour < 24) return `${diffHour} giờ trước`;

    return (
      d.toLocaleDateString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      }) +
      ' ' +
      d.toLocaleTimeString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit'
      })
    );
  }

  function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
      minimumFractionDigits: 0
    }).format(amount);
  }

  window.transactionHistory = {
    loadTransactionHistory,
    addTransaction,
    loadMoreTransactions
  };

  window.loadMore = loadMoreTransactions;

  window.addEventListener('storage', event => {
    if (event.key === STORAGE_KEY) {
      loadTransactionHistory();
    }
  });
})(window, document);
