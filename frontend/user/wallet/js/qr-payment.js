(function(window, document) {
  const MIN_AMOUNT = 10000;
  const MAX_AMOUNT = 10000000;
  const PROCESSING_CLASS = 'processing-message';
  const ERROR_CLASS = 'error-message';

  function init() {
    const amountInput = document.getElementById('topupAmount');
    if (!amountInput) {
      return;
    }

    amountInput.addEventListener('input', handleAmountInput);
    amountInput.addEventListener('change', handleAmountInput);

    handleAmountInput({ target: amountInput });
  }

  function handleAmountInput(event) {
    const input = event.target;
    const value = parseInt(input.value, 10);

    if (!validateAmount(value, input)) {
      clearCanvas();
      showError(`Số tiền hợp lệ từ ${formatCurrency(MIN_AMOUNT)} đến ${formatCurrency(MAX_AMOUNT)}.`);
      return;
    }

    clearError();
    generate(value);
  }

  function validateAmount(amount, inputEl) {
    const valid = Number.isFinite(amount) && amount >= MIN_AMOUNT && amount <= MAX_AMOUNT;

    if (inputEl) {
      inputEl.setCustomValidity(
        valid
          ? ''
          : `Vui lòng nhập số tiền từ ${MIN_AMOUNT.toLocaleString()} ₫ đến ${MAX_AMOUNT.toLocaleString()} ₫`
      );
    }

    return valid;
  }

  function generate(amount) {
    const container = document.getElementById('qrCode');
    if (!container) {
      return;
    }

    container.innerHTML = '';

    const canvas = document.createElement('canvas');
    const qrSize = 200;
    const moduleSize = 8;
    const modules = qrSize / moduleSize;

    canvas.width = qrSize;
    canvas.height = qrSize;

    const ctx = canvas.getContext('2d');

    for (let row = 0; row < modules; row += 1) {
      for (let col = 0; col < modules; col += 1) {
        const isFilled = Math.random() > 0.4;
        ctx.fillStyle = isFilled ? '#000' : '#fff';
        ctx.fillRect(col * moduleSize, row * moduleSize, moduleSize, moduleSize);
      }
    }

    drawCornerSquare(ctx, 0, 0, moduleSize);
    drawCornerSquare(ctx, modules - 7, 0, moduleSize);
    drawCornerSquare(ctx, 0, modules - 7, moduleSize);

    ctx.fillStyle = '#fff';
    ctx.fillRect(qrSize / 2 - 45, qrSize / 2 - 18, 90, 36);
    ctx.fillStyle = '#111827';
    ctx.font = 'bold 12px Inter, Arial';
    ctx.textAlign = 'center';
    ctx.fillText(formatCurrency(Math.abs(amount)), qrSize / 2, qrSize / 2 + 4);

    container.appendChild(canvas);
  }

  function drawCornerSquare(ctx, x, y, moduleSize) {
    ctx.fillStyle = '#000';
    ctx.fillRect(x * moduleSize, y * moduleSize, 7 * moduleSize, 7 * moduleSize);

    ctx.fillStyle = '#fff';
    ctx.fillRect((x + 1) * moduleSize, (y + 1) * moduleSize, 5 * moduleSize, 5 * moduleSize);

    ctx.fillStyle = '#000';
    ctx.fillRect((x + 2) * moduleSize, (y + 2) * moduleSize, 3 * moduleSize, 3 * moduleSize);
  }

  function showProcessingMessage() {
    const container = document.querySelector('.qr-container');
    if (!container) {
      return;
    }

    clearProcessingMessage();

    const wrapper = document.createElement('div');
    wrapper.className = PROCESSING_CLASS;
    wrapper.innerHTML = `
      <div class="qr-processing">
        <div class="loading-spinner"></div>
        <p>Đang chờ thanh toán...</p>
        <p class="qr-processing-note">Đây là bản mô phỏng. Giao dịch sẽ hoàn tất sau vài giây.</p>
      </div>
    `;

    container.appendChild(wrapper);
  }

  function clearProcessingMessage() {
    const existing = document.querySelector(`.${PROCESSING_CLASS}`);
    if (existing && existing.parentNode) {
      existing.parentNode.removeChild(existing);
    }
  }

  function clearCanvas() {
    const container = document.getElementById('qrCode');
    if (container) {
      container.innerHTML = '';
    }
  }

  function showError(message) {
    const container = document.querySelector('.qr-container');
    if (!container) {
      return;
    }

    clearError();

    const errorDiv = document.createElement('div');
    errorDiv.className = ERROR_CLASS;
    errorDiv.textContent = message;
    container.appendChild(errorDiv);
  }

  function clearError() {
    const existing = document.querySelector(`.${ERROR_CLASS}`);
    if (existing && existing.parentNode) {
      existing.parentNode.removeChild(existing);
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

})(window, document);

(function (window, document) {

  function init() {
    bindEditBankInfo();
    bindSaveBankInfo();
    bindCancelBankInfo();
    bindWithdraw();
    loadBankInfo();
  }

  // Hiển thị form nhập bank
  function bindEditBankInfo() {
    const editBtn = document.querySelector('[data-action="edit-bank-info"]');
    const form = document.getElementById('bankInfoForm');
    const display = document.getElementById('bankInfoDisplay');

    if (!editBtn || !form || !display) return;

    editBtn.addEventListener('click', function () {
      display.classList.add('hidden');
      form.classList.remove('hidden');
    });
  }

  // Lưu thông tin ngân hàng
  function bindSaveBankInfo() {
    const saveBtn = document.querySelector('[data-action="save-bank-info"]');
    if (!saveBtn) return;

    saveBtn.addEventListener('click', function () {
      const account = document.getElementById('inputAccount').value.trim();
      const bank = document.getElementById('inputBank').value.trim();
      const name = document.getElementById('inputName').value.trim();

      if (!account || !bank || !name) {
        alert('Vui lòng nhập đầy đủ thông tin ngân hàng');
        return;
      }

      const bankInfo = { account, bank, name };
      localStorage.setItem('bankInfo', JSON.stringify(bankInfo));

      alert('Đã lưu thông tin ngân hàng');

      document.getElementById('bankInfoForm').classList.add('hidden');
      document.getElementById('bankInfoDisplay').classList.remove('hidden');

      renderBankInfo(bankInfo);
    });
  }

  // Hủy nhập
  function bindCancelBankInfo() {
    const cancelBtn = document.querySelector('[data-action="cancel-bank-info"]');
    if (!cancelBtn) return;

    cancelBtn.addEventListener('click', function () {
      document.getElementById('bankInfoForm').classList.add('hidden');
      document.getElementById('bankInfoDisplay').classList.remove('hidden');
    });
  }

  // Load bank info khi vào trang
  function loadBankInfo() {
    const bankInfo = localStorage.getItem('bankInfo');
    if (!bankInfo) return;

    renderBankInfo(JSON.parse(bankInfo));
  }

  // Hiển thị bank info
  function renderBankInfo(bankInfo) {
    document.getElementById('userAccount').innerText = bankInfo.account;
    document.getElementById('userBank').innerText = bankInfo.bank;
    document.getElementById('userName').innerText = bankInfo.name;
  }

  // Xác nhận rút tiền
  function bindWithdraw() {
    const withdrawBtn = document.querySelector('[data-action="confirm-withdraw"]');
    if (!withdrawBtn) return;

    withdrawBtn.addEventListener('click', function () {
      const bankInfo = localStorage.getItem('bankInfo');

      if (!bankInfo) {
        alert('Vui lòng cập nhật thông tin ngân hàng trước khi rút tiền');
        return;
      }

      alert('Yêu cầu rút tiền đã được gửi');
    });
  }

  window.initWallet = init;

})(window, document);
(function (window, document) {

  function init() {
    const withdrawSection = document.getElementById('withdrawSection');

    if (localStorage.getItem('openWithdraw') === 'true') {
      if (withdrawSection) {
        withdrawSection.classList.remove('hidden');
      }
      localStorage.removeItem('openWithdraw');
    }
  }

  window.initTopup = init;

})(window, document);
document.addEventListener('DOMContentLoaded', function () {
  const payBtn = document.getElementById('payBtn'); // nút Thanh toán
  const qrPopup = document.getElementById('qrPopup');
  const paymentMethods = document.querySelectorAll('.payment-method');

  let selectedMethod = 'wallet';

  paymentMethods.forEach(method => {
    method.addEventListener('click', function () {
      paymentMethods.forEach(m => m.classList.remove('active'));
      this.classList.add('active');
      selectedMethod = this.dataset.paymentMethod;
    });
  });

  if (payBtn) {
    payBtn.addEventListener('click', function () {
      if (selectedMethod === 'bankqr') {
        qrPopup.classList.remove('hidden');
      } else {
        alert('Thanh toán bằng số dư ví');
      }
    });
  }

  // Đóng popup
  document.querySelectorAll('[data-action="close-qr"]').forEach(btn => {
    btn.addEventListener('click', () => {
      qrPopup.classList.add('hidden');
    });
  });

  // Copy
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      navigator.clipboard.writeText(this.dataset.copyValue);
      alert('Đã sao chép');
    });
  });

  // Xác nhận đã thanh toán
  document.querySelector('[data-action="confirm-paid"]')
    ?.addEventListener('click', function () {
      alert('Hệ thống sẽ kiểm tra giao dịch');
      qrPopup.classList.add('hidden');
    });
});
