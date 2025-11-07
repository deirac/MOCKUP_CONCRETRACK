// Plants Page JavaScript Module
const Plants = (function() {
    // Private variables
    let plantsTableBody;
    let plantsLoading;
    let plantsEmpty;

    // Private methods
    function initPlantsPage() {
        plantsTableBody = document.getElementById('plants-table-body');
        plantsLoading = document.getElementById('plants-loading');
        plantsEmpty = document.getElementById('plants-empty');
    }

    function showLoading() {
        if (plantsLoading) plantsLoading.classList.remove('d-none');
        if (plantsTableBody) plantsTableBody.innerHTML = '';
        if (plantsEmpty) plantsEmpty.classList.add('d-none');
    }

    function hideLoading() {
        if (plantsLoading) plantsLoading.classList.add('d-none');
    }

    function showEmptyState() {
        if (plantsEmpty) plantsEmpty.classList.remove('d-none');
        if (plantsTableBody) plantsTableBody.innerHTML = '';
    }

    function displayPlantsData(plants) {
        if (!plantsTableBody) return;

        if (!plants || plants.length === 0) {
            showEmptyState();
            return;
        }

        let plantsHTML = '';

        plants.forEach(plant => {
            const statusBadge = getStatusBadge(plant.status);
            const mixesHTML = plant.mixes_available.map(mix => 
                `<span class="badge mix-badge me-1">${mix}</span>`
            ).join('');

            plantsHTML += `
                <tr class="fade-in">
                    <td>
                        <strong>${plant.name}</strong>
                    </td>
                    <td>${plant.location}</td>
                    <td>
                        <span class="fw-bold">${plant.capacity}</span>
                        <small class="text-muted"> m³/h</small>
                    </td>
                    <td>${statusBadge}</td>
                    <td>${mixesHTML}</td>
                    <td>
                        <span class="fw-bold">${plant.transport}</span>
                        <small class="text-muted"> disponibles</small>
                    </td>
                    <td>${plant.manager}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary btn-action" 
                                onclick="Plants.viewPlantDetails(${plant.id})"
                                title="Ver detalles">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning btn-action" 
                                onclick="Plants.editPlant(${plant.id})"
                                title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                    </td>
                </tr>
            `;
        });

        plantsTableBody.innerHTML = plantsHTML;
        hideLoading();
    }

    function getStatusBadge(status) {
        const statusMap = {
            'active': { class: 'status-active', text: 'Activa' },
            'maintenance': { class: 'status-maintenance', text: 'Mantenimiento' },
            'inactive': { class: 'status-inactive', text: 'Inactiva' }
        };

        const statusInfo = statusMap[status] || { class: 'bg-secondary', text: status };
        return `<span class="status-badge ${statusInfo.class}">${statusInfo.text}</span>`;
    }

    function displayPlantDetails(plant) {
        const modalBody = document.getElementById('plantModalBody');
        if (!modalBody) return;

        const lastMaintenance = new Date(plant.last_maintenance).toLocaleDateString();
        const mixesHTML = plant.mixes_available.map(mix => 
            `<span class="badge mix-badge me-1 mb-1">${mix}</span>`
        ).join('');

        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Nombre</div>
                        <div class="plant-detail-value">${plant.name}</div>
                    </div>
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Ubicación</div>
                        <div class="plant-detail-value">${plant.location}</div>
                    </div>
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Capacidad</div>
                        <div class="plant-detail-value">${plant.capacity} m³/h</div>
                    </div>
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Estado</div>
                        <div class="plant-detail-value">${getStatusBadge(plant.status)}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Encargado</div>
                        <div class="plant-detail-value">${plant.manager}</div>
                    </div>
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Contacto</div>
                        <div class="plant-detail-value">
                            <div>${plant.phone}</div>
                            <div>${plant.email}</div>
                        </div>
                    </div>
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Último Mantenimiento</div>
                        <div class="plant-detail-value">${lastMaintenance}</div>
                    </div>
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Transporte</div>
                        <div class="plant-detail-value">${plant.transport}</div>
                    </div>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Mezclas Disponibles</div>
                        <div class="plant-detail-value">${mixesHTML}</div>
                    </div>
                </div>
            </div>
            ${plant.notes ? `
            <div class="row mt-3">
                <div class="col-12">
                    <div class="plant-detail-item">
                        <div class="plant-detail-label">Notas</div>
                        <div class="plant-detail-value">${plant.notes}</div>
                    </div>
                </div>
            </div>
            ` : ''}
        `;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('plantModal'));
        modal.show();
    }

    // Public methods
    return {
        init: function() {
            document.addEventListener('DOMContentLoaded', function() {
                initPlantsPage();
            });
        },

        loadPlantsSummary: async function() {
            try {
                const data = await apiCall('/api/v1/plants-summary');
                document.getElementById('total-plants').textContent = data.total_plants;
                document.getElementById('active-plants').textContent = data.active_plants;
                document.getElementById('total-capacity').textContent = data.total_capacity;
                document.getElementById('available-trucks').textContent = data.available_trucks;
            } catch (error) {
                console.error('Error loading plants summary:', error);
            }
        },

        loadPlantsData: async function() {
            showLoading();
            try {
                const data = await apiCall('/api/plants');
                displayPlantsData(data.data);
            } catch (error) {
                console.error('Error loading plants data:', error);
                showEmptyState();
            }
        },

        viewPlantDetails: async function(plantId) {
            try {
                const data = await apiCall(`/api/plants/${plantId}`);
                displayPlantDetails(data.data);
            } catch (error) {
                console.error('Error loading plant details:', error);
                showNotification('Error al cargar los detalles de la planta', 'error');
            }
        },

        editPlant: function(plantId) {
            showNotification(`Función de edición para planta ${plantId} - En desarrollo`, 'info');
        }
    };
})();

// Auto-initialize
Plants.init();