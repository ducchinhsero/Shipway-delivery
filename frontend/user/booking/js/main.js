/* =====================================================
   1. KHAI BÁO BIẾN & CẤU HÌNH
===================================================== */
const input = document.getElementById("product-image");
const preview = document.getElementById("imagePreview");
const counter = document.getElementById("imageCounter");
const form = document.querySelector(".order-form");
const confirmBtn = document.getElementById("confirmBtn");

const MAX_IMAGES = 5; // Increased to 5 as per API
let images = [];

if (counter) counter.style.display = "none";

// API Configuration
const API_BASE_URL = window.location.origin;

// Vehicle pricing config
const PRICING_CONFIG = {
  bike: { base_fee: 15000, per_km: 3000, max_weight: 30 },
  car: { base_fee: 30000, per_km: 5000, max_weight: 300 },
  van: { base_fee: 50000, per_km: 7000, max_weight: 500 },
  truck_500kg: { base_fee: 80000, per_km: 10000, max_weight: 500 },
  truck_1000kg: { base_fee: 120000, per_km: 15000, max_weight: 1000 }
};

/* =====================================================
   2. ĐỊNH DẠNG TIỀN TỆ
===================================================== */
document.querySelectorAll(".price-input").forEach(el => {
  el.addEventListener("input", e => {
    let raw = e.target.value.replace(/\D/g, "");
    e.target.value = raw ? parseInt(raw).toLocaleString("vi-VN") : "";
  });
});

/* =====================================================
   3. CHẶN NHẬP CHỮ (SỐ)
===================================================== */
document
  .querySelectorAll(".weight-input, .size-input")
  .forEach(input => {
    input.addEventListener("keypress", e => {
      if (!/[0-9.]/.test(e.key)) e.preventDefault();
      if (e.key === "." && input.value.includes(".")) e.preventDefault();
    });
  });

/* =====================================================
   4. UPLOAD + RESIZE + PREVIEW ẢNH
===================================================== */
if (input) {
  input.addEventListener("change", () => {
    const files = Array.from(input.files);

    if (images.length + files.length > MAX_IMAGES) {
      alert(`Chỉ được upload tối đa ${MAX_IMAGES} ảnh`);
      input.value = "";
      return;
    }

    files.forEach(file => {
      resizeImage(file, 225, 225, blob => {
        images.push({
          blob,
          url: URL.createObjectURL(blob)
        });
        renderPreview();
      });
    });

    input.value = "";
  });
}

function renderPreview() {
  preview.innerHTML = "";

  if (images.length === 0) {
    counter.style.display = "none";
  } else {
    counter.style.display = "block";
    counter.textContent = `${images.length}/${MAX_IMAGES}`;
  }

  images.forEach((item, index) => {
    const div = document.createElement("div");
    div.className = "preview-item";
    div.innerHTML = `
      <img src="${item.url}" alt="preview">
      <button type="button" class="btn-remove-img">×</button>
    `;

    div.querySelector(".btn-remove-img").onclick = () => {
      images.splice(index, 1);
      renderPreview();
    };

    preview.appendChild(div);
  });
}

function resizeImage(file, w, h, cb) {
  const reader = new FileReader();
  reader.onload = e => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      canvas.getContext("2d").drawImage(img, 0, 0, w, h);
      canvas.toBlob(blob => cb(blob), "image/jpeg", 0.9);
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

/* =====================================================
   5. VALIDATION UI
===================================================== */
function showErrorMessage(container, text) {
  if (container.querySelector(".error-message")) return;

  const msg = document.createElement("div");
  msg.className = "error-message";
  msg.textContent = text;
  container.appendChild(msg);
}

function resetValidation() {
  document.querySelectorAll(".input-error").forEach(el =>
    el.classList.remove("input-error")
  );
  document.querySelectorAll(".error-message").forEach(el => el.remove());
}

/* =====================================================
   6. TÍNH KHOẢNG CÁCH (HAVERSINE)
===================================================== */
function calculateDistance(lat1, lng1, lat2, lng2) {
  const R = 6371; // Earth radius in km
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLng / 2) * Math.sin(dLng / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

/* =====================================================
   7. TÍNH PHÍ SHIPPING
===================================================== */
function calculateShippingFee() {
  const pickupLat = parseFloat(document.querySelector('[name="pickup_lat"]').value);
  const pickupLng = parseFloat(document.querySelector('[name="pickup_lng"]').value);
  const dropoffLat = parseFloat(document.querySelector('[name="dropoff_lat"]').value);
  const dropoffLng = parseFloat(document.querySelector('[name="dropoff_lng"]').value);
  const weight = parseFloat(document.querySelector('[name="weight"]').value);
  const vehicleType = document.querySelector('[name="vehicle_type"]').value;
  const codAmountStr = document.querySelector('[name="cod_amount"]').value.replace(/\./g, "");
  const codAmount = parseFloat(codAmountStr) || 0;

  const estimatedFeeEl = document.getElementById("estimatedFee");

  // Validate inputs
  if (!pickupLat || !pickupLng || !dropoffLat || !dropoffLng || !weight || !vehicleType) {
    estimatedFeeEl.textContent = "Nhập đầy đủ thông tin để tính phí";
    estimatedFeeEl.style.color = "#666";
    return;
  }

  // Check weight limit
  const config = PRICING_CONFIG[vehicleType];
  if (weight > config.max_weight) {
    estimatedFeeEl.textContent = `Khối lượng vượt quá giới hạn ${config.max_weight}kg cho loại xe này`;
    estimatedFeeEl.style.color = "#dc2626";
    return;
  }

  // Calculate distance
  const distance = calculateDistance(pickupLat, pickupLng, dropoffLat, dropoffLng);
  document.getElementById("distanceValue").textContent = distance.toFixed(2) + " km";

  // Calculate fee
  let shippingFee = config.base_fee + (distance * config.per_km);
  
  // Weight surcharge (for weight > 50kg on certain vehicles)
  if (weight > 50 && vehicleType !== "bike") {
    const surchargeRate = { car: 500, van: 400, truck_500kg: 300, truck_1000kg: 200 }[vehicleType] || 0;
    shippingFee += (weight - 50) * surchargeRate;
  }

  // COD fee (1% of COD, max 50,000)
  if (codAmount > 0) {
    const codFee = Math.min(codAmount * 0.01, 50000);
    shippingFee += codFee;
  }

  // Round to nearest 1000
  shippingFee = Math.ceil(shippingFee / 1000) * 1000;

  estimatedFeeEl.textContent = shippingFee.toLocaleString("vi-VN") + " VNĐ";
  estimatedFeeEl.style.color = "#0b3cc1";
}

/* =====================================================
   8. SUBMIT API
===================================================== */
async function submitOrder() {
  const formData = new FormData();

  // Pickup info
  formData.append("pickup_address", document.querySelector('[name="pickup_address"]').value.trim());
  formData.append("pickup_lat", document.querySelector('[name="pickup_lat"]').value.trim());
  formData.append("pickup_lng", document.querySelector('[name="pickup_lng"]').value.trim());
  formData.append("pickup_contact_name", document.querySelector('[name="pickup_contact_name"]').value.trim());
  formData.append("pickup_contact_phone", document.querySelector('[name="pickup_contact_phone"]').value.trim());
  formData.append("pickup_note", document.querySelector('[name="pickup_note"]').value.trim() || "");

  // Dropoff info
  formData.append("dropoff_address", document.querySelector('[name="dropoff_address"]').value.trim());
  formData.append("dropoff_lat", document.querySelector('[name="dropoff_lat"]').value.trim());
  formData.append("dropoff_lng", document.querySelector('[name="dropoff_lng"]').value.trim());
  formData.append("dropoff_contact_name", document.querySelector('[name="dropoff_contact_name"]').value.trim());
  formData.append("dropoff_contact_phone", document.querySelector('[name="dropoff_contact_phone"]').value.trim());
  formData.append("dropoff_note", document.querySelector('[name="dropoff_note"]').value.trim() || "");

  // Product info
  formData.append("product_name", document.querySelector('[name="product_name"]').value.trim());
  formData.append("weight", document.querySelector('[name="weight"]').value.trim());
  
  const length = document.querySelector('[name="length"]').value.trim();
  const width = document.querySelector('[name="width"]').value.trim();
  const height = document.querySelector('[name="height"]').value.trim();
  
  if (length) formData.append("length", length);
  if (width) formData.append("width", width);
  if (height) formData.append("height", height);

  formData.append("vehicle_type", document.querySelector('[name="vehicle_type"]').value);
  formData.append("note", document.querySelector('[name="note"]').value.trim() || "");

  const codAmountStr = document.querySelector('[name="cod_amount"]').value.replace(/\./g, "");
  formData.append("cod_amount", codAmountStr || "0");

  // Images
  images.forEach((img, i) => {
    formData.append("images", img.blob, `product_${i}.jpg`);
  });

  const token = localStorage.getItem("access_token");

  try {
    const res = await fetch(`${API_BASE_URL}/api/v1/orders`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      console.error(err);
      alert(err.detail || "Tạo đơn thất bại");
      return;
    }

    const result = await res.json();
    alert(result.message || "Tạo đơn thành công!");
    
    // Redirect to booking details page with order_id
    window.location.href = `../booking-details/index.html?order_id=${result.order_id}`;

  } catch (err) {
    console.error(err);
    alert("Không thể kết nối server");
  }
}

/* =====================================================
   9. AUTO CALCULATE FEE ON INPUT CHANGE
===================================================== */
const calcTriggers = ['pickup_lat', 'pickup_lng', 'dropoff_lat', 'dropoff_lng', 'weight', 'vehicle_type', 'cod_amount'];
calcTriggers.forEach(name => {
  const el = document.querySelector(`[name="${name}"]`);
  if (el) {
    el.addEventListener('input', calculateShippingFee);
    el.addEventListener('change', calculateShippingFee);
  }
});

/* =====================================================
   10. CLICK XÁC NHẬN – VALIDATE
===================================================== */
if (confirmBtn) {
  confirmBtn.addEventListener("click", e => {
    e.preventDefault();
    resetValidation();

    let isValid = true;

    /* --- ẢNH (optional now) --- */
    // Images are now optional, so we don't validate them

    /* --- INPUT --- */
    form.querySelectorAll("input[data-required], select[data-required]").forEach(input => {
      const val = input.value.trim();
      const parent = input.closest('.form-group');

      if (!val) {
        isValid = false;
        input.classList.add("input-error");
        showErrorMessage(parent, "Trường này không được để trống");
        return;
      }

      // Validate numeric fields
      if (input.classList.contains("weight-input") || input.classList.contains("size-input")) {
        if (isNaN(val) || parseFloat(val) <= 0) {
          isValid = false;
          input.classList.add("input-error");
          showErrorMessage(parent, "Vui lòng nhập số hợp lệ");
        }
      }

      // Validate phone numbers
      if (input.name.includes("phone")) {
        const phoneRegex = /^(0|\+84)[0-9]{9,10}$/;
        if (!phoneRegex.test(val)) {
          isValid = false;
          input.classList.add("input-error");
          showErrorMessage(parent, "Số điện thoại không hợp lệ");
        }
      }

      // Validate coordinates
      if (input.name.includes("lat")) {
        const lat = parseFloat(val);
        if (isNaN(lat) || lat < -90 || lat > 90) {
          isValid = false;
          input.classList.add("input-error");
          showErrorMessage(parent, "Vĩ độ không hợp lệ (-90 đến 90)");
        }
      }

      if (input.name.includes("lng")) {
        const lng = parseFloat(val);
        if (isNaN(lng) || lng < -180 || lng > 180) {
          isValid = false;
          input.classList.add("input-error");
          showErrorMessage(parent, "Kinh độ không hợp lệ (-180 đến 180)");
        }
      }
    });

    if (!isValid) {
      document
        .querySelector(".input-error, .error-message")
        ?.scrollIntoView({ behavior: "smooth", block: "center" });
      return;
    }

    submitOrder();
  });
}
