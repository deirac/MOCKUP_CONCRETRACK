// Orders Page JavaScript Module
const Orders = (function() {
    // Private variables
    let ordersTableBody;
    let ordersLoading;
    let ordersEmpty;
    let allOrders = [];
    let filteredOrders = [];

    // Private methods
    function initOrdersPage() {
        ordersTableBody = document.getElementById('orders-table-body');
        ordersLoading = document.getElementById('orders-loading');
        ordersEmpty = document.getElementById('orders-empty');
    }

    function showLoading() {
        if (ordersLoading) ordersLoading.classList.remove('d-none');
        if (ordersTableBody) ordersTableBody.innerHTML = '';
        if (ordersEmpty) ordersEmpty.classList.add('d-none');
    }

    function hideLoading() {
        if (ordersLoading) ordersLoading.classList.add('d-none');
    }

    function showEmptyState() {
        if (ordersEmpty) ordersEmpty.classList.remove('d-none');
        if (ordersTableBody) ordersTableBody.innerHTML = '';
    }

    function displayOrdersData(orders) {
        if (!ordersTableBody) return;

        if (!orders || orders.length === 0) {
            showEmptyState();
            return;
        }

        let ordersHTML = '';

        orders.forEach(order => {
            const statusBadge = getStatusBadge(order.status);
            const priorityBadge = getPriorityBadge(order.priority);
            const scheduledTime = new Date(order.scheduled_time);
            const isPast = scheduledTime < new Date();
            const timeClass = isPast ? 'past' : 'future';
            const timeFormatted = scheduledTime.toLocaleString('es-ES');

            ordersHTML += `
                <tr class="fade-in">
                    <td>
                        <strong>#${order.id}</strong>
                    </td>
                    <td>
                        <div class="fw-bold">${order.project_name}</div>
                        <small class="text-muted">${order.address}</small>
                    </td>
                    <td>${order.client}</td>
                    <td>
                        <span class="badge mix-badge">${order.mix_type}</span>
                    </td>
                    <td>
                        <span class="volume-indicator">${order.volume}</span>
                        <small class="text-muted"> m³</small>
                    </td>
                    <td>${statusBadge}</td>
                    <td>
                        <span class="scheduled-time ${timeClass}">${timeFormatted}</span>
                    </td>
                    <td>${priorityBadge}</td>
                    <td>${order.assigned_plant}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary btn-action" 
                                onclick="Orders.viewOrderDetails(${order.id})"
                                title="Ver detalles">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning btn-action" 
                                onclick="Orders.updateOrderStatus(${order.id})"
                                title="Cambiar estado">
                            <i class="bi bi-arrow-repeat"></i>
                        </button>
                        ${order.status !== 'completed' && order.status !== 'cancelled' ? `
                        <button class="btn btn-sm btn-outline-success btn-action" 
                                onclick="Orders.completeOrder(${order.id})"
                                title="Completar orden">
                            <i class="bi bi-check-circle"></i>
                        </button>
                        ` : ''}
                    </td>
                </tr>
            `;
        });

        ordersTableBody.innerHTML = ordersHTML;
        hideLoading();
    }

    function getStatusBadge(status) {
        const statusMap = {
            'scheduled': { class: 'status-scheduled', text: 'Programada' },
            'preparing': { class: 'status-preparing', text: 'Preparando' },
            'in_progress': { class: 'status-in_progress', text: 'En Progreso' },
            'completed': { class: 'status-completed', text: 'Completada' },
            'cancelled': { class: 'status-cancelled', text: 'Cancelada' }
        };

        const statusInfo = statusMap[status] || { class: 'bg-secondary', text: status };
        return `<span class="status-badge ${statusInfo.class}">${statusInfo.text}</span>`;
    }

    function getPriorityBadge(priority) {
        const priorityMap = {
            'high': { class: 'priority-high', text: 'Alta' },
            'medium': { class: 'priority-medium', text: 'Media' },
            'low': { class: 'priority-low', text: 'Baja' }
        };

        const priorityInfo = priorityMap[priority] || { class: 'bg-secondary', text: priority };
        return `<span class="priority-badge ${priorityInfo.class}">${priorityInfo.text}</span>`;
    }

    function displayOrderDetails(order) {
        const modalBody = document.getElementById('orderModalBody');
        if (!modalBody) return;

        const scheduledTime = new Date(order.scheduled_time).toLocaleString('es-ES');
        const createdTime = new Date(order.created_at).toLocaleString('es-ES');
        const completedTime = order.completed_at ? new Date(order.completed_at).toLocaleString('es-ES') : 'N/A';

        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <div class="order-detail-item">
                        <div class="order-detail-label">ID de Orden</div>
                        <div class="order-detail-value">#${order.id}</div>
                    </div>
                    <div class="order-detail-item">
                        <div class="order-detail-label">Proyecto</div>
                        <div class="order-detail-value">${order.project_name}</div>
                    </div>
                    <div class="order-detail-item">
                        <div class="order-detail-label">Cliente</div>
                        <div class="order-detail-value">${order.client}</div>
                    </div>
                    <div class="order-detail-item">
                        <div class="order-detail-label">Estado</div>
                        <div class="order-detail-value">${getStatusBadge(order.status)}</div>
                    </div>
                    <div class="order-detail-item">
                        <div class="order-detail-label">Prioridad</div>
                        <div class="order-detail-value">${getPriorityBadge(order.priority)}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="order-detail-item">
                        <div class="order-detail-label">Tipo de Mezcla</div>
                        <div class="order-detail-value"><span class="badge mix-badge">${order.mix_type}</span></div>
                    </div>
                    <div class="order-detail-item">
                        <div class="order-detail-label">Volumen</div>
                        <div class="order-detail-value">${order.volume} m³</div>
                    </div>
                    <div class="order-detail-item">
                        <div class="order-detail-label">Duración Estimada</div>
                        <div class="order-detail-value">${order.estimated_duration} horas</div>
                    </div>
                    <div class="order-detail-item">
                        <div class="order-detail-label">Planta Asignada</div>
                        <div class="order-detail-value">${order.assigned_plant}</div>
                    </div>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-md-6">
                    <div class="order-detail-item">
                        <div class="order-detail-label">Programada para</div>
                        <div class="order-detail-value">${scheduledTime}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="order-detail-item">
                        <div class="order-detail-label">Creada el</div>
                        <div class="order-detail-value">${createdTime}</div>
                    </div>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <div class="order-detail-item">
                        <div class="order-detail-label">Dirección de Entrega</div>
                        <div class="order-detail-value">${order.address}</div>
                    </div>
                </div>
            </div>
            ${order.notes ? `
            <div class="row mt-3">
                <div class="col-12">
                    <div class="order-detail-item">
                        <div class="order-detail-label">Notas</div>
                        <div class="order-detail-value">${order.notes}</div>
                    </div>
                </div>
            </div>
            ` : ''}
            ${order.completed_at ? `
            <div class="row mt-3">
                <div class="col-12">
                    <div class="order-detail-item">
                        <div class="order-detail-label">Completada el</div>
                        <div class="order-detail-value">${completedTime}</div>
                    </div>
                </div>
            </div>
            ` : ''}
        `;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('orderModal'));
        modal.show();
    }

    function applyFilters() {
        const statusFilter = document.getElementById('status-filter').value;
        const priorityFilter = document.getElementById('priority-filter').value;
        const dateFilter = document.getElementById('date-filter').value;

        filteredOrders = allOrders.filter(order => {
            // Status filter
            if (statusFilter !== 'all' && order.status !== statusFilter) {
                return false;
            }
            
            // Priority filter
            if (priorityFilter !== 'all' && order.priority !== priorityFilter) {
                return false;
            }
            
            // Date filter
            if (dateFilter) {
                const orderDate = new Date(order.scheduled_time).toISOString().split('T')[0];
                if (orderDate !== dateFilter) {
                    return false;
                }
            }
            
            return true;
        });

        displayOrdersData(filteredOrders);
    }

    // Public methods
    return {
        init: function() {
            document.addEventListener('DOMContentLoaded', function() {
                initOrdersPage();
            });
        },

        loadOrdersSummary: async function() {
            try {
                const data = await apiCall('/api/v1/orders-summary');
                document.getElementById('total-orders').textContent = data.total_orders;
                document.getElementById('active-orders').textContent = data.active_orders;
                document.getElementById('volume-today').textContent = data.total_volume_today;
                document.getElementById('urgent-orders').textContent = data.urgent_orders;
            } catch (error) {
                console.error('Error loading orders summary:', error);
            }
        },

        loadOrdersData: async function() {
            showLoading();
            try {
                const data = await apiCall('/api/orders');
                allOrders = data.data;
                filteredOrders = [...allOrders];
                displayOrdersData(filteredOrders);
            } catch (error) {
                console.error('Error loading orders data:', error);
                showEmptyState();
            }
        },

        loadProjects: async function() {
            try {
                const data = await apiCall('/api/v1/projects');
                const projectSelect = document.getElementById('project-select');
                
                if (projectSelect && data) {
                    projectSelect.innerHTML = '<option value="">Seleccionar proyecto...</option>';
                    data.forEach(project => {
                        const option = document.createElement('option');
                        option.value = project.id;
                        option.textContent = `${project.name} - ${project.client}`;
                        projectSelect.appendChild(option);
                    });
                }
            } catch (error) {
                console.error('Error loading projects:', error);
            }
        },

        filterOrders: function() {
            applyFilters();
        },

        clearFilters: function() {
            document.getElementById('status-filter').value = 'all';
            document.getElementById('priority-filter').value = 'all';
            document.getElementById('date-filter').value = '';
            filteredOrders = [...allOrders];
            displayOrdersData(filteredOrders);
        },

        viewOrderDetails: async function(orderId) {
            try {
                const data = await apiCall(`/api/orders/${orderId}`);
                displayOrderDetails(data.data);
            } catch (error) {
                console.error('Error loading order details:', error);
                showNotification('Error al cargar los detalles de la orden', 'error');
            }
        },

        showCreateModal: function() {
            const modal = new bootstrap.Modal(document.getElementById('createOrderModal'));
            modal.show();
        },

        createOrder: async function() {
            try {
                const formData = {
                    project_id: parseInt(document.getElementById('project-select').value),
                    mix_type: document.getElementById('mix-type').value,
                    volume: parseFloat(document.getElementById('volume').value),
                    scheduled_time: document.getElementById('scheduled-time').value,
                    address: document.getElementById('address').value,
                    priority: document.getElementById('priority').value,
                    assigned_plant: document.getElementById('assigned-plant').value,
                    estimated_duration: parseFloat(document.getElementById('duration').value),
                    notes: document.getElementById('notes').value
                };

                // Basic validation
                if (!formData.project_id || !formData.mix_type || !formData.volume || !formData.scheduled_time || !formData.address || !formData.assigned_plant || !formData.estimated_duration) {
                    showNotification('Por favor completa todos los campos requeridos', 'error');
                    return;
                }

                const data = await apiCall('/api/orders', {
                    method: 'POST',
                    body: JSON.stringify(formData)
                });

                showNotification('Orden creada exitosamente', 'success');
                
                // Close modal and refresh data
                const modal = bootstrap.Modal.getInstance(document.getElementById('createOrderModal'));
                modal.hide();
                
                this.loadOrdersSummary();
                this.loadOrdersData();
                
            } catch (error) {
                console.error('Error creating order:', error);
                showNotification('Error al crear la orden', 'error');
            }
        },

        updateOrderStatus: async function(orderId) {
            const newStatus = prompt('Ingresa el nuevo estado (scheduled, preparing, in_progress, completed, cancelled):');
            if (newStatus && ['scheduled', 'preparing', 'in_progress', 'completed', 'cancelled'].includes(newStatus)) {
                try {
                    const formData = new FormData();
                    formData.append('status', newStatus);

                    await apiCall(`/api/orders/${orderId}/status`, {
                        method: 'PUT',
                        body: formData
                    });

                    showNotification('Estado de orden actualizado', 'success');
                    this.loadOrdersSummary();
                    this.loadOrdersData();
                } catch (error) {
                    console.error('Error updating order status:', error);
                    showNotification('Error al actualizar el estado', 'error');
                }
            }
        },

        completeOrder: async function(orderId) {
            try {
                const formData = new FormData();
                formData.append('status', 'completed');

                await apiCall(`/api/orders/${orderId}/status`, {
                    method: 'PUT',
                    body: formData
                });

                showNotification('Orden marcada como completada', 'success');
                this.loadOrdersSummary();
                this.loadOrdersData();
            } catch (error) {
                console.error('Error completing order:', error);
                showNotification('Error al completar la orden', 'error');
            }
        }
    };
})();

// Auto-initialize
Orders.init();