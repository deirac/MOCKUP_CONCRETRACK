// Inventory Page JavaScript Module
const Inventory = (function() {
    // Private variables
    let inventoryTableBody;
    let inventoryLoading;
    let inventoryEmpty;
    let allMaterials = [];
    let filteredMaterials = [];
    let currentMaterialId = null;

    // Private methods
    function initInventoryPage() {
        inventoryTableBody = document.getElementById('inventory-table-body');
        inventoryLoading = document.getElementById('inventory-loading');
        inventoryEmpty = document.getElementById('inventory-empty');
    }

    function showLoading() {
        if (inventoryLoading) inventoryLoading.classList.remove('d-none');
        if (inventoryTableBody) inventoryTableBody.innerHTML = '';
        if (inventoryEmpty) inventoryEmpty.classList.add('d-none');
    }

    function hideLoading() {
        if (inventoryLoading) inventoryLoading.classList.add('d-none');
    }

    function showEmptyState() {
        if (inventoryEmpty) inventoryEmpty.classList.remove('d-none');
        if (inventoryTableBody) inventoryTableBody.innerHTML = '';
    }

    function displayInventoryData(materials) {
        if (!inventoryTableBody) return;

        if (!materials || materials.length === 0) {
            showEmptyState();
            return;
        }

        let inventoryHTML = '';

        materials.forEach(material => {
            const statusBadge = getStatusBadge(material.status);
            const stockPercentage = (material.current_stock / material.max_stock) * 100;
            const stockClass = getStockClass(material.status);
            const progressClass = getProgressClass(material.status);
            const totalValue = material.current_stock * material.cost_per_unit;
            const lastRestock = new Date(material.last_restock).toLocaleDateString('es-ES');

            inventoryHTML += `
                <tr class="fade-in ${material.status === 'critical' ? 'pulse-critical' : ''}">
                    <td>
                        <div class="d-flex align-items-center">
                            <div class="material-icon material-${material.name.toLowerCase()}">
                                <i class="bi bi-box"></i>
                            </div>
                            <div>
                                <strong>${material.name}</strong>
                                <div class="supplier-info">${material.description}</div>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="stock-indicator ${stockClass}">${material.current_stock}</div>
                        <div class="stock-progress">
                            <div class="stock-progress-bar ${progressClass}" 
                                 style="width: ${stockPercentage}%">
                            </div>
                        </div>
                        <div class="progress-text ${stockClass}">${Math.round(stockPercentage)}%</div>
                    </td>
                    <td>
                        <small class="text-muted">${material.min_stock} / ${material.max_stock}</small>
                        <div class="unit">${material.unit}</div>
                    </td>
                    <td>${statusBadge}</td>
                    <td class="supplier-info">${material.supplier}</td>
                    <td>
                        <span class="cost-display">$${material.cost_per_unit.toFixed(2)}</span>
                        <div class="unit">/${material.unit}</div>
                    </td>
                    <td>
                        <span class="material-value">$${totalValue.toFixed(2)}</span>
                    </td>
                    <td class="last-restock">${lastRestock}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary btn-action" 
                                onclick="Inventory.viewMaterialDetails(${material.id})"
                                title="Ver detalles">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning btn-action" 
                                onclick="Inventory.showUpdateStockModal(${material.id})"
                                title="Actualizar stock">
                            <i class="bi bi-arrow-up-down"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-info btn-action" 
                                onclick="Inventory.viewMaterialUsage(${material.id})"
                                title="Ver uso">
                            <i class="bi bi-graph-up"></i>
                        </button>
                    </td>
                </tr>
            `;
        });

        inventoryTableBody.innerHTML = inventoryHTML;
        hideLoading();
    }

    function getStatusBadge(status) {
        const statusMap = {
            'critical': { class: 'status-critical', text: 'Crítico' },
            'low': { class: 'status-low', text: 'Bajo' },
            'optimal': { class: 'status-optimal', text: 'Óptimo' },
            'high': { class: 'status-high', text: 'Alto' }
        };

        const statusInfo = statusMap[status] || { class: 'bg-secondary', text: status };
        return `<span class="status-badge ${statusInfo.class}">${statusInfo.text}</span>`;
    }

    function getStockClass(status) {
        const classMap = {
            'critical': 'stock-critical',
            'low': 'stock-low',
            'optimal': 'stock-optimal',
            'high': 'stock-high'
        };
        return classMap[status] || 'stock-optimal';
    }

    function getProgressClass(status) {
        const classMap = {
            'critical': 'stock-progress-critical',
            'low': 'stock-progress-low',
            'optimal': 'stock-progress-optimal',
            'high': 'stock-progress-high'
        };
        return classMap[status] || 'stock-progress-optimal';
    }

    function getMaterialIconClass(materialName) {
        const iconMap = {
            'ARENA': 'material-arena',
            'AGUA': 'material-agua',
            'ADT1': 'material-adt',
            'ADT2': 'material-adt',
            'CMTO': 'material-cmto',
            'ADIC': 'material-adic',
            'GRAVA': 'material-grava'
        };
        return iconMap[materialName] || 'material-arena';
    }

    function displayMaterialDetails(material) {
        const modalBody = document.getElementById('materialModalBody');
        if (!modalBody) return;

        const lastRestock = new Date(material.last_restock).toLocaleString('es-ES');
        const stockPercentage = (material.current_stock / material.max_stock) * 100;
        const totalValue = material.current_stock * material.cost_per_unit;

        modalBody.innerHTML = `
            <div class="material-card ${material.status} p-3 mb-4">
                <div class="row">
                    <div class="col-md-6">
                        <div class="material-detail-item">
                            <div class="material-detail-label">Nombre del Material</div>
                            <div class="material-detail-value">${material.name}</div>
                        </div>
                        <div class="material-detail-item">
                            <div class="material-detail-label">Descripción</div>
                            <div class="material-detail-value">${material.description}</div>
                        </div>
                        <div class="material-detail-item">
                            <div class="material-detail-label">Proveedor</div>
                            <div class="material-detail-value">${material.supplier}</div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="material-detail-item">
                            <div class="material-detail-label">Estado</div>
                            <div class="material-detail-value">${getStatusBadge(material.status)}</div>
                        </div>
                        <div class="material-detail-item">
                            <div class="material-detail-label">Unidad</div>
                            <div class="material-detail-value">${material.unit}</div>
                        </div>
                        <div class="material-detail-item">
                            <div class="material-detail-label">Última Recarga</div>
                            <div class="material-detail-value">${lastRestock}</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-md-6">
                    <div class="material-detail-item">
                        <div class="material-detail-label">Stock Actual</div>
                        <div class="material-detail-value">
                            <span class="stock-indicator ${getStockClass(material.status)}">
                                ${material.current_stock} ${material.unit}
                            </span>
                        </div>
                    </div>
                    <div class="material-detail-item">
                        <div class="material-detail-label">Límites de Stock</div>
                        <div class="material-detail-value">
                            Mín: ${material.min_stock} ${material.unit} | 
                            Máx: ${material.max_stock} ${material.unit}
                        </div>
                    </div>
                    <div class="material-detail-item">
                        <div class="material-detail-label">Progreso de Stock</div>
                        <div class="material-detail-value">
                            <div class="stock-progress">
                                <div class="stock-progress-bar ${getProgressClass(material.status)}" 
                                     style="width: ${stockPercentage}%">
                                </div>
                            </div>
                            <div class="progress-text ${getStockClass(material.status)}">
                                ${Math.round(stockPercentage)}% del máximo
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="material-detail-item">
                        <div class="material-detail-label">Costo Unitario</div>
                        <div class="material-detail-value">
                            <span class="cost-display">$${material.cost_per_unit.toFixed(2)}</span> / ${material.unit}
                        </div>
                    </div>
                    <div class="material-detail-item">
                        <div class="material-detail-label">Valor Total en Inventario</div>
                        <div class="material-detail-value">
                            <span class="material-value">$${totalValue.toFixed(2)}</span>
                        </div>
                    </div>
                    <div class="material-detail-item">
                        <div class="material-detail-label">Días hasta agotarse*</div>
                        <div class="material-detail-value">
                            <span class="${getStockClass(material.status)}">
                                ${calculateDaysRemaining(material)}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            ${material.notes ? `
            <div class="material-detail-item">
                <div class="material-detail-label">Notas Adicionales</div>
                <div class="material-detail-value">${material.notes}</div>
            </div>
            ` : ''}

            <div class="text-center mt-4">
                <button class="btn btn-warning me-2" onclick="Inventory.showUpdateStockModal(${material.id})">
                    <i class="bi bi-arrow-up-down me-2"></i>
                    Actualizar Stock
                </button>
                <button class="btn btn-info" onclick="Inventory.viewMaterialUsage(${material.id})">
                    <i class="bi bi-graph-up me-2"></i>
                    Ver Estadísticas de Uso
                </button>
            </div>

            <div class="mt-3 text-muted small">
                * Estimación basada en uso promedio histórico
            </div>
        `;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('materialModal'));
        modal.show();
    }

    function calculateDaysRemaining(material) {
        // Esta es una estimación simple - en una app real usarías datos históricos
        const usageRates = {
            'ARENA': 50,  // m³ por día
            'AGUA': 25,   // m³ por día
            'ADT1': 30,   // kg por día
            'ADT2': 15,   // kg por día
            'CMTO': 200,  // kg por día
            'ADIC': 5,    // kg por día
            'GRAVA': 40   // m³ por día
        };

        const dailyUsage = usageRates[material.name] || 10;
        const daysRemaining = material.current_stock / dailyUsage;
        
        if (daysRemaining < 7) return '< 1 semana';
        if (daysRemaining < 30) return Math.round(daysRemaining / 7) + ' semanas';
        return Math.round(daysRemaining / 30) + ' meses';
    }

    function applyFilters() {
        const statusFilter = document.getElementById('status-filter')?.value || 'all';

        filteredMaterials = allMaterials.filter(material => {
            // Status filter
            if (statusFilter !== 'all' && material.status !== statusFilter) {
                return false;
            }
            
            return true;
        });

        displayInventoryData(filteredMaterials);
    }

    // Public methods
    return {
        init: function() {
            document.addEventListener('DOMContentLoaded', function() {
                initInventoryPage();
            });
        },

        loadInventorySummary: async function() {
            try {
                const data = await apiCall('/api/v1/inventory-summary');
                document.getElementById('total-materials').textContent = data.total_materials;
                document.getElementById('total-value').textContent = '$' + data.total_inventory_value.toLocaleString();
                document.getElementById('critical-materials').textContent = data.needs_restock;
                document.getElementById('optimal-materials').textContent = data.optimal_materials;
            } catch (error) {
                console.error('Error loading inventory summary:', error);
            }
        },

        loadInventoryData: async function() {
            showLoading();
            try {
                const data = await apiCall('/api/inventory');
                allMaterials = data.data;
                filteredMaterials = [...allMaterials];
                displayInventoryData(filteredMaterials);
            } catch (error) {
                console.error('Error loading inventory data:', error);
                showEmptyState();
            }
        },

        filterByStatus: function(status) {
            filteredMaterials = allMaterials.filter(material => material.status === status);
            displayInventoryData(filteredMaterials);
        },

        clearFilters: function() {
            filteredMaterials = [...allMaterials];
            displayInventoryData(filteredMaterials);
        },

        viewMaterialDetails: async function(materialId) {
            try {
                const data = await apiCall(`/api/inventory/${materialId}`);
                displayMaterialDetails(data.data);
            } catch (error) {
                console.error('Error loading material details:', error);
                showNotification('Error al cargar los detalles del material', 'error');
            }
        },

        showUpdateStockModal: function(materialId) {
            currentMaterialId = materialId;
            const material = allMaterials.find(m => m.id === materialId);
            if (material) {
                document.getElementById('new-stock').value = material.current_stock;
                document.getElementById('stock-unit').textContent = `Unidad: ${material.unit}`;
                document.getElementById('updateStockModalLabel').textContent = `Actualizar Stock - ${material.name}`;
            }
            const modal = new bootstrap.Modal(document.getElementById('updateStockModal'));
            modal.show();
        },

        updateStock: async function() {
            if (!currentMaterialId) return;

            const newStock = parseFloat(document.getElementById('new-stock').value);
            if (isNaN(newStock) || newStock < 0) {
                showNotification('Por favor ingresa un valor válido para el stock', 'error');
                return;
            }

            try {
                const formData = new FormData();
                formData.append('new_stock', newStock);

                await apiCall(`/api/inventory/${currentMaterialId}/stock`, {
                    method: 'PUT',
                    body: formData
                });

                showNotification('Stock actualizado exitosamente', 'success');
                
                // Close modal and refresh data
                const modal = bootstrap.Modal.getInstance(document.getElementById('updateStockModal'));
                modal.hide();
                
                this.loadInventorySummary();
                this.loadInventoryData();
                
            } catch (error) {
                console.error('Error updating stock:', error);
                showNotification('Error al actualizar el stock', 'error');
            }
        },

        calculateRequirements: function() {
            const modal = new bootstrap.Modal(document.getElementById('requirementsModal'));
            modal.show();
        },

        calculateMaterialRequirements: async function() {
            const mixType = document.getElementById('mix-type-calc').value;
            const volume = parseFloat(document.getElementById('volume-calc').value);

            if (!mixType || isNaN(volume) || volume <= 0) {
                showNotification('Por favor completa todos los campos correctamente', 'error');
                return;
            }

            try {
                // En una implementación real, esto llamaría a la API
                // Por ahora simulamos la respuesta
                const requirements = {
                    'ARENA': volume * 700,
                    'AGUA': volume * 170,
                    'ADT1': volume * 4,
                    'ADT2': volume * 2,
                    'CMTO': volume * 400,
                    'GRAVA': volume * 1000
                };

                let resultHTML = '';
                let allAvailable = true;

                for (const [materialName, requiredQty] of Object.entries(requirements)) {
                    const material = allMaterials.find(m => m.name === materialName);
                    const isAvailable = material && material.current_stock >= requiredQty;
                    const status = material ? (isAvailable ? 'available' : 'insufficient') : 'not_found';
                    
                    if (!isAvailable) allAvailable = false;

                    resultHTML += `
                        <tr class="${status === 'available' ? 'requirement-available' : status === 'insufficient' ? 'requirement-insufficient' : 'requirement-not-found'}">
                            <td><strong>${materialName}</strong></td>
                            <td>${requiredQty.toFixed(2)} ${material?.unit || 'unidades'}</td>
                            <td>${material ? `${material.current_stock} ${material.unit}` : 'No encontrado'}</td>
                            <td>
                                <span class="availability-badge availability-${status}">
                                    ${status === 'available' ? 'Disponible' : status === 'insufficient' ? 'Insuficiente' : 'No encontrado'}
                                </span>
                            </td>
                        </tr>
                    `;
                }

                document.getElementById('requirements-table-body').innerHTML = resultHTML;
                document.getElementById('requirements-result').classList.remove('d-none');

                if (allAvailable) {
                    showNotification('Todos los materiales están disponibles', 'success');
                } else {
                    showNotification('Algunos materiales no están disponibles en cantidad suficiente', 'warning');
                }

            } catch (error) {
                console.error('Error calculating requirements:', error);
                showNotification('Error al calcular los requerimientos', 'error');
            }
        },

        viewMaterialUsage: async function(materialId) {
            try {
                const data = await apiCall(`/api/inventory/${materialId}/usage`);
                const material = data.data.material;
                
                let usageHTML = `
                    <div class="usage-stats">
                        <h4>Estadísticas de Uso - ${material.name}</h4>
                        <div class="usage-item">
                            <span>Total usado (última semana):</span>
                            <strong>${data.data.total_used_week.toFixed(2)} ${material.unit}</strong>
                        </div>
                        <div class="usage-item">
                            <span>Uso promedio diario:</span>
                            <strong>${data.data.avg_daily_usage.toFixed(2)} ${material.unit}/día</strong>
                        </div>
                        <div class="usage-item">
                            <span>Días de stock restante:</span>
                            <strong>${Math.round(data.data.days_remaining)} días</strong>
                        </div>
                    </div>
                `;

                if (data.data.recent_usage && data.data.recent_usage.length > 0) {
                    usageHTML += `
                        <h6>Uso Reciente:</h6>
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Fecha</th>
                                        <th>Cantidad</th>
                                        <th>Proyecto</th>
                                        <th>Mezcla</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.data.recent_usage.map(usage => `
                                        <tr>
                                            <td>${new Date(usage.date).toLocaleDateString('es-ES')}</td>
                                            <td>${usage.quantity_used} ${material.unit}</td>
                                            <td>${usage.project}</td>
                                            <td>${usage.mix_type}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    `;
                }

                // Mostrar en el modal de detalles
                const modalBody = document.getElementById('materialModalBody');
                if (modalBody) {
                    modalBody.innerHTML = usageHTML;
                } else {
                    // Si no hay modal abierto, mostrar en alerta
                    showNotification(`Uso de ${material.name}: ${data.data.total_used_week} ${material.unit} en la última semana`, 'info');
                }

            } catch (error) {
                console.error('Error loading material usage:', error);
                showNotification('Error al cargar las estadísticas de uso', 'error');
            }
        }
    };
})();

// Auto-initialize
Inventory.init();