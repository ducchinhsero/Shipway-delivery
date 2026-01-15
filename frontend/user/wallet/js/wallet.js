// Wallet functionality and page orchestration

(function(window, document) {
  const BALANCE_KEY = 'walletBalance';
  const ORDER_KEY = 'currentOrder';
  const USER_ID_KEY = 'userId';
  const PAYMENT_METHOD_KEY = 'selectedPaymentMethod';

  let currentBalance = 0;
  let refreshIntervalId = null;

  document.addEventListener('DOMContentLoaded', () => {
    const body = document.body || {};
    const pageType = body.dataset ? body.dataset.page : 'wallet-overview';

    loadWalletBalance();

    switch (pageType) {
      case 'wallet-topup':
        initTopupPage();
        break;
      case 'wallet-payment':
        initPaymentPage();
        break;
      case 'wallet-overview':
      default:
        initWalletOverviewPage();
        break;
    }
  });

  function loadWalletBalance() {
    const storedBalance = parseFloat(localStorage.getItem(BALANCE_KEY) || '0');
    currentBalance = Number.isNaN(storedBalance) ? 0 : storedBalance;
    updateBalanceDisplays();
  }

  function updateBalanceDisplays() {
    const formatted = formatCurrency(currentBalance);

    const mainDisplay = document.getElementById('walletBalance');
    if (mainDisplay) {
      mainDisplay.textContent = formatted;
      mainDisplay.style.transform = 'scale(1.1)';
      setTimeout(() => {
        mainDisplay.style.transform = 'scale(1)';
      }, 200);
    }

    const secondaryDisplay = document.getElementById('walletBalanceDisplay');
    if (secondaryDisplay) {
      secondaryDisplay.textContent = formatted;
    }

    const availableBalanceEl = document.getElementById('availableBalance');
    if (availableBalanceEl) {
      availableBalanceEl.textContent = formatted;
    }

    localStorage.setItem(BALANCE_KEY, currentBalance.toString());
  }

  function initWalletOverviewPage() {
    if (refreshIntervalId) {
      clearInterval(refreshIntervalId);
    }

    refreshIntervalId = setInterval(loadWalletBalance, 30000);

    const gotoTopupButton = document.querySelector('[data-action="goto-topup"]');
    if (gotoTopupButton) {
      gotoTopupButton.addEventListener('click', () => {
        window.location.href = 'topup.html';
      });
    }

    const loadMoreButton = document.querySelector('[data-action="load-more-transactions"]');
    if (loadMoreButton) {
      loadMoreButton.addEventListener('click', () => {
        if (window.transactionHistory) {
          window.transactionHistory.loadMoreTransactions();
        }
      });
    }

    const payButtons = document.querySelectorAll('[data-pay-order]');
    payButtons.forEach(button => {
      button.addEventListener('click', event => {
        const target = event.currentTarget.dataset;
        if (!target.orderId || !target.orderAmount) {
          return;
        }

        const orderPayload = {
          orderId: target.orderId,
          amount: Number(target.orderAmount),
          destination: target.orderDestination || ''
        };

        localStorage.setItem(ORDER_KEY, JSON.stringify(orderPayload));
        window.location.href = 'payment.html';
      });
    });

    if (window.transactionHistory) {
      window.transactionHistory.loadTransactionHistory();
    }
  }

  function initTopupPage() {
    const state = {
      selectedMethod: 'qr',
      activeTab: 'topup',
      userId: getOrCreateUserId()
    };

    if (window.qrPayment && typeof window.qrPayment.init === 'function') {
      window.qrPayment.init();
    }

    attachTopupTabHandlers(state);
    attachMethodHandlers(state);
    attachPresetHandlers();
    attachWithdrawPresetHandlers();
    attachCopyHandlers();
    attachTopupActionHandlers(state);

    updateTransferContent(state.userId);
    updateBalanceDisplays();

    // Ensure QR preview renders with default amount
    const amountInput = document.getElementById('topupAmount');
    if (amountInput && window.qrPayment && typeof window.qrPayment.generate === 'function') {
      //window.qrPayment.generate(amountInput.value);
      amountInput.addEventListener('input', () => {
        if (state.selectedMethod === 'qr') {
          //window.qrPayment.generate(amountInput.value);
        }
      });
    }
  }

  function initPaymentPage() {
    const order = getStoredOrder();
    if (!order) {
      alert('Không tìm thấy thông tin đơn hàng.');
      window.location.href = 'index.html';
      return;
    }

    populateOrderDetails(order);
    setupPaymentMethodSelection();
    setupProcessPayment(order);
    updateBalanceDisplays();
  }

  function attachTopupTabHandlers(state) {
    const tabButtons = document.querySelectorAll('[data-topup-tab]');
    tabButtons.forEach(button => {
      button.addEventListener('click', event => {
        const tab = event.currentTarget.dataset.topupTab;
        if (!tab || tab === state.activeTab) {
          return;
        }

        state.activeTab = tab;
        tabButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.topupTab === tab));

        const topupSection = document.getElementById('topupSection');
        const withdrawSection = document.getElementById('withdrawSection');

        if (topupSection && withdrawSection) {
          topupSection.classList.toggle('hidden', tab !== 'topup');
          withdrawSection.classList.toggle('hidden', tab !== 'withdraw');
        }

        if (tab === 'withdraw') {
          updateBalanceDisplays();
        }
      });
    });
  }

  function attachMethodHandlers(state) {
    const methodButtons = document.querySelectorAll('[data-topup-method]');
    const qrSection = document.getElementById('qrSection');
    const visaSection = document.getElementById('visaSection');

    methodButtons.forEach(button => {
      button.addEventListener('click', event => {
        const method = event.currentTarget.dataset.topupMethod;
        if (!method || method === state.selectedMethod) {
          return;
        }

        state.selectedMethod = method;
        methodButtons.forEach(btn => btn.classList.toggle('active', btn.dataset.topupMethod === method));

        if (qrSection && visaSection) {
          qrSection.classList.toggle('hidden', method !== 'qr');
          visaSection.classList.toggle('hidden', method !== 'visa');
        }

        const amountInput = document.getElementById('topupAmount');
        if (method === 'qr' && amountInput && window.qrPayment && typeof window.qrPayment.generate === 'function') {
          window.qrPayment.generate(amountInput.value);
        }
      });
    });
  }

  function attachPresetHandlers() {
    const presets = document.querySelectorAll('[data-amount-preset]');
    const amountInput = document.getElementById('topupAmount');

    if (!amountInput) {
      return;
    }

    presets.forEach(button => {
      button.addEventListener('click', event => {
        const value = parseInt(event.currentTarget.dataset.amountPreset, 10);
        if (!value) {
          return;
        }

        amountInput.value = value;
        presets.forEach(btn => btn.classList.toggle('active', btn === event.currentTarget));

        if (window.qrPayment && typeof window.qrPayment.generate === 'function') {
          window.qrPayment.generate(value);
        }
      });
    });
  }

  function attachWithdrawPresetHandlers() {
    const presets = document.querySelectorAll('[data-withdraw-preset]');
    const withdrawInput = document.getElementById('withdrawAmount');

    if (!withdrawInput) {
      return;
    }

    presets.forEach(button => {
      button.addEventListener('click', event => {
        const value = parseInt(event.currentTarget.dataset.withdrawPreset, 10);
        if (!value) {
          return;
        }

        withdrawInput.value = value;
        presets.forEach(btn => btn.classList.toggle('active', btn === event.currentTarget));
      });
    });
  }

  function attachCopyHandlers() {
    const copyButtons = document.querySelectorAll('[data-copy-value]');
    copyButtons.forEach(button => {
      button.addEventListener('click', event => {
        const value = event.currentTarget.dataset.copyValue;
        if (!value) {
          return;
        }

        navigator.clipboard.writeText(value).then(() => {
          alert(`Đã sao chép: ${value}`);
        }).catch(err => {
          console.error('Không thể sao chép', err);
        });
      });
    });
  }

  function attachTopupActionHandlers(state) {
    const topupButton = document.querySelector('[data-action="confirm-topup"]');
    const withdrawButton = document.querySelector('[data-action="confirm-withdraw"]');
    const goWalletButton = document.querySelector('[data-action="go-wallet"]');

    if (topupButton) {
      topupButton.addEventListener('click', () => handleTopup(state));
    }

    if (withdrawButton) {
      withdrawButton.addEventListener('click', handleWithdrawal);
    }

    if (goWalletButton) {
      goWalletButton.addEventListener('click', () => {
        window.location.href = 'index.html';
      });
    }
  }

  function handleTopup(state) {
    const amountInput = document.getElementById('topupAmount');
    const amount = amountInput ? parseInt(amountInput.value, 10) : 0;

    if (!amount || amount < 10000) {
      alert('Số tiền không hợp lệ. Vui lòng nhập tối thiểu 10.000 ₫');
      return;
    }

    if (state.selectedMethod === 'visa' && !validateVisaFields()) {
      alert('Vui lòng nhập đầy đủ thông tin thẻ Visa');
      return;
    }

    showProcessingState('Đang xử lý thanh toán...');

    if (state.selectedMethod === 'qr' && window.qrPayment && typeof window.qrPayment.showProcessingMessage === 'function') {
      window.qrPayment.showProcessingMessage();
    }

    setTimeout(() => {
      const description = state.selectedMethod === 'qr'
        ? 'Nạp tiền qua QR ngân hàng'
        : 'Nạp tiền qua Visa';

      addBalance(amount);
      recordTransaction({
        title: description,
        amount,
        type: 'credit',
        status: 'success'
      });

      showSuccessState(`Nạp tiền thành công ${formatCurrency(amount)}`);

      if (window.qrPayment && typeof window.qrPayment.clearProcessingMessage === 'function') {
        window.qrPayment.clearProcessingMessage();
      }

      updateBalanceDisplays();
    }, 5000);
  }

  function handleWithdrawal() {
    const withdrawInput = document.getElementById('withdrawAmount');
    const amount = withdrawInput ? parseInt(withdrawInput.value, 10) : 0;

    if (!amount || amount < 50000) {
      alert('Số tiền rút tối thiểu là 50.000 ₫');
      return;
    }

    if (amount > currentBalance) {
      alert('Số dư không đủ để thực hiện giao dịch');
      return;
    }

    const userAccount = document.getElementById('userAccount');
    if (userAccount && userAccount.textContent === 'Chưa cập nhật') {
      alert('Vui lòng cập nhật thông tin tài khoản ngân hàng trước khi rút tiền');
      return;
    }

    showProcessingState('Đang xử lý yêu cầu rút tiền...');

    setTimeout(() => {
      const success = deductBalance(amount);
      if (!success) {
        alert('Số dư không đủ để rút tiền');
        hideProcessingState();
        return;
      }

      recordTransaction({
        title: 'Rút tiền về tài khoản ngân hàng',
        amount,
        type: 'debit',
        status: 'success'
      });

      const message = `Rút tiền thành công ${formatCurrency(amount)}. Tiền sẽ về tài khoản trong vòng 1-2 ngày làm việc.`;
      showSuccessState(message);
      updateBalanceDisplays();
    }, 5000);
  }

  function validateVisaFields() {
    const number = document.getElementById('cardNumber');
    const name = document.getElementById('cardName');
    const expiry = document.getElementById('cardExpiry');
    const cvv = document.getElementById('cardCvv');

    return [number, name, expiry, cvv].every(input => input && input.value.trim().length > 0);
  }

  function showProcessingState(message) {
    const paymentStatus = document.getElementById('paymentStatus');
    const successStatus = document.getElementById('successStatus');
    const statusMessage = document.getElementById('statusMessage');
    const successMessage = document.getElementById('successMessage');

    if (successStatus) {
      successStatus.classList.add('hidden');
    }

    if (paymentStatus) {
      paymentStatus.classList.remove('hidden');
    }

    if (statusMessage) {
      statusMessage.textContent = message;
    }

    if (successMessage) {
      successMessage.textContent = '';
    }
  }

  function showSuccessState(message) {
    const paymentStatus = document.getElementById('paymentStatus');
    const successStatus = document.getElementById('successStatus');
    const successMessage = document.getElementById('successMessage');

    if (paymentStatus) {
      paymentStatus.classList.add('hidden');
    }

    if (successStatus) {
      successStatus.classList.remove('hidden');
    }

    if (successMessage) {
      successMessage.textContent = message;
    }
  }

  function hideProcessingState() {
    const paymentStatus = document.getElementById('paymentStatus');
    if (paymentStatus) {
      paymentStatus.classList.add('hidden');
    }
  }

  function setupPaymentMethodSelection() {
    const paymentMethods = document.querySelectorAll('.payment-method');
    let selectedMethod = localStorage.getItem(PAYMENT_METHOD_KEY) || 'wallet';

    paymentMethods.forEach(method => {
      const methodName = method.dataset.paymentMethod;
      method.classList.toggle('active', methodName === selectedMethod);

      method.addEventListener('click', () => {
        selectedMethod = method.dataset.paymentMethod || 'wallet';
        localStorage.setItem(PAYMENT_METHOD_KEY, selectedMethod);

        paymentMethods.forEach(item => {
          item.classList.toggle('active', item === method);
        });
      });
    });
  }

  function setupProcessPayment(order) {
    const processButton = document.querySelector('[data-action="process-payment"]');
    if (!processButton) {
      return;
    }

    const paymentStatus = document.getElementById('paymentStatus');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const statusMessage = document.getElementById('statusMessage');

    processButton.addEventListener('click', () => {
      const selectedMethod = (document.querySelector('.payment-method.active') || {}).dataset?.paymentMethod || 'wallet';

      if (selectedMethod === 'wallet' && order.amount > currentBalance) {
        alert('Số dư tài khoản không đủ, vui lòng nạp thêm tiền');
        window.location.href = 'index.html';
        return;
      }

      if (paymentStatus) {
        paymentStatus.classList.remove('hidden');
      }

      if (loadingSpinner) {
        loadingSpinner.style.display = 'block';
      }

      if (statusMessage) {
        statusMessage.textContent = 'Đang xử lý thanh toán...';
      }

      setTimeout(() => {
        let successMessage = '';

        if (selectedMethod === 'wallet') {
          deductBalance(order.amount);
          successMessage = `Thanh toán thành công! ${formatCurrency(order.amount)} đã được trừ từ ví.`;
        } else if (selectedMethod === 'visa') {
          successMessage = `Thanh toán thành công qua Visa! ${formatCurrency(order.amount)}`;
        } else {
          successMessage = `Thanh toán thành công qua QR Ngân hàng! ${formatCurrency(order.amount)}`;
        }

        recordTransaction({
          title: `Thanh toán ${order.orderId}`,
          amount: order.amount,
          type: 'debit',
          status: 'success',
          method: selectedMethod
        });

        if (loadingSpinner) {
          loadingSpinner.style.display = 'none';
        }

        if (statusMessage) {
          statusMessage.textContent = successMessage;
        }

        localStorage.removeItem(ORDER_KEY);

        setTimeout(() => {
          window.location.href = 'index.html';
        }, 2000);
      }, 5000);
    });
  }

  function populateOrderDetails(order) {
    const orderIdEl = document.getElementById('orderId');
    const shippingFeeEl = document.getElementById('shippingFee');
    const totalAmountEl = document.getElementById('totalAmount');

    if (orderIdEl) {
      orderIdEl.textContent = order.orderId;
    }

    if (shippingFeeEl) {
      shippingFeeEl.textContent = formatCurrency(order.amount);
    }

    if (totalAmountEl) {
      totalAmountEl.textContent = formatCurrency(order.amount);
    }
  }

  function getStoredOrder() {
    try {
      const raw = localStorage.getItem(ORDER_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (error) {
      console.error('Không thể đọc dữ liệu đơn hàng:', error);
      return null;
    }
  }

  function getOrCreateUserId() {
    let userId = localStorage.getItem(USER_ID_KEY);
    if (!userId) {
      userId = `ID${Math.floor(100000 + Math.random() * 900000)}`;
      localStorage.setItem(USER_ID_KEY, userId);
    }
    return userId;
  }

  function updateTransferContent(userId) {
    const transferContent = document.getElementById('transferContent');
    if (!transferContent) {
      return;
    }

    const now = new Date();
    const dateStr = `${String(now.getDate()).padStart(2, '0')}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getFullYear()).slice(-2)}`;
    transferContent.textContent = `${userId}_${dateStr}`;
  }

  function recordTransaction(transaction) {
    if (window.transactionHistory && typeof window.transactionHistory.addTransaction === 'function') {
      window.transactionHistory.addTransaction(transaction);
    } else {
      // Fallback persistence
      const stored = JSON.parse(localStorage.getItem('transactions') || '[]');
      stored.unshift({
        id: transaction.id || Date.now(),
        title: transaction.title,
        amount: transaction.amount,
        type: transaction.type,
        date: (transaction.date instanceof Date ? transaction.date.toISOString() : transaction.date || new Date().toISOString()),
        status: transaction.status || 'completed'
      });
      localStorage.setItem('transactions', JSON.stringify(stored));
    }
  }

  function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount || 0);
  }

  function showSuccessNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #4CAF50;
      color: white;
      padding: 16px 24px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      z-index: 1001;
      font-weight: 600;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 3000);
  }

  function addBalance(amount) {
    currentBalance += amount;
    updateBalanceDisplays();
    showSuccessNotification(`Nạp tiền thành công: ${formatCurrency(amount)}`);
  }

  function deductBalance(amount) {
    if (currentBalance < amount) {
      return false;
    }

    currentBalance -= amount;
    updateBalanceDisplays();
    return true;
  }

  function refreshBalance() {
    loadWalletBalance();
  }

  function getCurrentBalance() {
    return currentBalance;
  }

  function showError(message) {
    console.error(message);
  }

  window.walletUtils = {
    getCurrentBalance,
    refreshBalance,
    addBalance,
    deductBalance,
    formatCurrency
  };
})(window, document);
