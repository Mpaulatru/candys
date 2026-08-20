// ClaroVenta - Main JS

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide icons if available
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // Mobile menu toggle
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileNav = document.getElementById('mobile-nav');
  
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', () => {
      mobileNav.classList.toggle('hidden');
    });
  }

  // Upload zone interactions
  const uploadZone = document.getElementById('upload-zone');
  const fileInput = document.getElementById('csv-input');
  const fileNameDisplay = document.getElementById('file-name');
  const uploadFeedback = document.getElementById('upload-feedback');

  if (uploadZone && fileInput) {
    // Click to open file picker
    uploadZone.addEventListener('click', () => fileInput.click());

    // Drag & drop
    ['dragenter', 'dragover'].forEach(event => {
      uploadZone.addEventListener(event, (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(event => {
      uploadZone.addEventListener(event, (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
      });
    });

    uploadZone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files.length) handleFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length) handleFile(e.target.files[0]);
    });
  }

  function handleFile(file) {
    if (!file.name.endsWith('.csv')) {
      showFeedback('Por favor sube un archivo CSV', 'error');
      return;
    }

    if (fileNameDisplay) {
      fileNameDisplay.textContent = file.name;
      fileNameDisplay.classList.remove('hidden');
    }

    showFeedback('Archivo cargado correctamente. Procesando...', 'success');

    // Simulate processing
    setTimeout(() => {
      showFeedback('¡Listo! Tus datos están listos para analizar.', 'success');
      const analyzeBtn = document.getElementById('analyze-btn');
      if (analyzeBtn) {
        analyzeBtn.disabled = false;
        analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
      }
    }, 1200);
  }

  function showFeedback(message, type) {
    if (!uploadFeedback) return;
    uploadFeedback.textContent = message;
    uploadFeedback.classList.remove('hidden', 'text-red-600', 'text-emerald-600');
    uploadFeedback.classList.add(type === 'error' ? 'text-red-600' : 'text-emerald-600');
  }

  // Manual product form - Add product row
  const addProductBtn = document.getElementById('add-product-btn');
  const productsContainer = document.getElementById('products-form');

  if (addProductBtn && productsContainer) {
    addProductBtn.addEventListener('click', () => {
      const index = productsContainer.children.length + 1;
      const row = document.createElement('div');
      row.className = 'grid grid-cols-1 sm:grid-cols-4 gap-3 p-4 bg-white border border-slate-200 rounded-xl fade-in';
      row.innerHTML = `
        <div>
          <label class="form-label">Producto</label>
          <input type="text" class="form-input" placeholder="Ej: Café Premium" name="product_${index}">
        </div>
        <div>
          <label class="form-label">Unidades vendidas</label>
          <input type="number" class="form-input" placeholder="0" name="units_${index}" min="0">
        </div>
        <div>
          <label class="form-label">Precio unitario</label>
          <input type="number" class="form-input" placeholder="0.00" name="price_${index}" min="0" step="0.01">
        </div>
        <div>
          <label class="form-label">Costo unitario</label>
          <input type="number" class="form-input" placeholder="0.00" name="cost_${index}" min="0" step="0.01">
        </div>
      `;
      productsContainer.appendChild(row);
      
      // Re-init icons if needed
      if (typeof lucide !== 'undefined') lucide.createIcons();
    });
  }

  // Toggle between CSV and Manual
  const tabCsv = document.getElementById('tab-csv');
  const tabManual = document.getElementById('tab-manual');
  const panelCsv = document.getElementById('panel-csv');
  const panelManual = document.getElementById('panel-manual');

  if (tabCsv && tabManual) {
    tabCsv.addEventListener('click', () => {
      tabCsv.classList.add('bg-primary', 'text-white');
      tabCsv.classList.remove('bg-white', 'text-slate-600');
      tabManual.classList.remove('bg-primary', 'text-white');
      tabManual.classList.add('bg-white', 'text-slate-600');
      panelCsv?.classList.remove('hidden');
      panelManual?.classList.add('hidden');
    });

    tabManual.addEventListener('click', () => {
      tabManual.classList.add('bg-primary', 'text-white');
      tabManual.classList.remove('bg-white', 'text-slate-600');
      tabCsv.classList.remove('bg-primary', 'text-white');
      tabCsv.classList.add('bg-white', 'text-slate-600');
      panelManual?.classList.remove('hidden');
      panelCsv?.classList.add('hidden');
    });
  }

  // Simple chart bars animation on dashboard
  const bars = document.querySelectorAll('.chart-bar');
  bars.forEach((bar, i) => {
    const height = bar.dataset.height || '50';
    bar.style.height = '0%';
    setTimeout(() => {
      bar.style.transition = 'height 0.6s ease';
      bar.style.height = height + '%';
    }, 100 + i * 80);
  });
});
