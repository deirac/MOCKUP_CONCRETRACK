// Checklist Page JavaScript Module
const Checklist = (function() {
    // Private variables
    let checklistsTableBody;
    let checklistsLoading;
    let checklistsEmpty;
    let allChecklists = [];
    let filteredChecklists = [];

    // Private methods
    function initChecklistPage() {
        checklistsTableBody = document.getElementById('checklists-table-body');
        checklistsLoading = document.getElementById('checklists-loading');
        checklistsEmpty = document.getElementById('checklists-empty');
    }

    function showLoading() {
        if (checklistsLoading) checklistsLoading.classList.remove('d-none');
        if (checklistsTableBody) checklistsTableBody.innerHTML = '';
        if (checklistsEmpty) checklistsEmpty.classList.add('d-none');
    }

    function hideLoading() {
        if (checklistsLoading) checklistsLoading.classList.add('d-none');
    }

    function showEmptyState() {
        if (checklistsEmpty) checklistsEmpty.classList.remove('d-none');
        if (checklistsTableBody) checklistsTableBody.innerHTML = '';
    }

    function displayChecklistsData(checklists) {
        if (!checklistsTableBody) return;

        if (!checklists || checklists.length === 0) {
            showEmptyState();
            return;
        }

        let checklistsHTML = '';

        checklists.forEach(checklist => {
            const statusBadge = getStatusBadge(checklist.status);
            const scheduledTime = new Date(checklist.scheduled_time);
            const timeFormatted = scheduledTime.toLocaleString('es-ES');
            
            const completedItems = checklist.items.filter(item => item.completed).length;
            const totalItems = checklist.items.length;
            const progressPercentage = totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;
            const progressClass = getProgressClass(progressPercentage);

            checklistsHTML += `
                <tr class="fade-in">
                    <td>
                        <strong>#${checklist.id}</strong>
                    </td>
                    <td>
                        <div class="fw-bold">${checklist.project_name}</div>
                        <small class="text-muted">Orden #${checklist.order_id}</small>
                    </td>
                    <td>${checklist.supervisor}</td>
                    <td>${timeFormatted}</td>
                    <td>${statusBadge}</td>
                    <td>
                        <div class="d-flex align-items-center">
                            <div class="progress flex-grow-1 me-2" style="height: 8px;">
                                <div class="progress-bar bg-success" role="progressbar" 
                                     style="width: ${progressPercentage}%">
                                </div>
                            </div>
                            <span class="progress-indicator ${progressClass}">${progressPercentage}%</span>
                        </div>
                    </td>
                    <td>
                        <span class="badge bg-light text-dark">${completedItems}/${totalItems}</span>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary btn-action" 
                                onclick="Checklist.viewChecklistDetails(${checklist.id})"
                                title="Ver detalles">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning btn-action" 
                                onclick="Checklist.editChecklist(${checklist.id})"
                                title="Editar">
                            <i class="bi bi-pencil"></i>
                        </button>
                        ${checklist.status !== 'completed' ? `
                        <button class="btn btn-sm btn-outline-success btn-action" 
                                onclick="Checklist.completeChecklist(${checklist.id})"
                                title="Completar checklist">
                            <i class="bi bi-check-circle"></i>
                        </button>
                        ` : ''}
                    </td>
                </tr>
            `;
        });

        checklistsTableBody.innerHTML = checklistsHTML;
        hideLoading();
    }

    function getStatusBadge(status) {
        const statusMap = {
            'pending': { class: 'status-pending', text: 'Pendiente' },
            'in_progress': { class: 'status-in_progress', text: 'En Progreso' },
            'completed': { class: 'status-completed', text: 'Completado' }
        };

        const statusInfo = statusMap[status] || { class: 'bg-secondary', text: status };
        return `<span class="status-badge ${statusInfo.class}">${statusInfo.text}</span>`;
    }

    function getProgressClass(percentage) {
        if (percentage >= 80) return 'high';
        if (percentage >= 50) return 'medium';
        return 'low';
    }

    function getCategoryBadge(category) {
        const categoryMap = {
            'pre_vaciado': { class: 'category-pre_vaciado', text: 'Pre-Vaciado' },
            'seguridad': { class: 'category-seguridad', text: 'Seguridad' },
            'calidad': { class: 'category-calidad', text: 'Calidad' },
            'post_vaciado': { class: 'category-post_vaciado', text: 'Post-Vaciado' }
        };

        const categoryInfo = categoryMap[category] || { class: 'bg-secondary', text: category };
        return `<span class="category-badge ${categoryInfo.class}">${categoryInfo.text}</span>`;
    }

    function displayChecklistDetails(checklist) {
        const modalBody = document.getElementById('checklistModalBody');
        if (!modalBody) return;

        const scheduledTime = new Date(checklist.scheduled_time).toLocaleString('es-ES');
        const createdTime = new Date(checklist.created_at).toLocaleString('es-ES');
        const completedTime = checklist.completed_at ? 
            new Date(checklist.completed_at).toLocaleString('es-ES') : 'No completado';

        const completedItems = checklist.items.filter(item => item.completed).length;
        const totalItems = checklist.items.length;
        const progressPercentage = totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;

        // Group items by category
        const itemsByCategory = {};
        checklist.items.forEach(item => {
            if (!itemsByCategory[item.category]) {
                itemsByCategory[item.category] = [];
            }
            itemsByCategory[item.category].push(item);
        });

        let itemsHTML = '';
        Object.keys(itemsByCategory).forEach(category => {
            const categoryItems = itemsByCategory[category];
            const categoryCompleted = categoryItems.filter(item => item.completed).length;
            const categoryTotal = categoryItems.length;
            const categoryPercentage = categoryTotal > 0 ? Math.round((categoryCompleted / categoryTotal) * 100) : 0;

            itemsHTML += `
                <div class="category-section">
                    <div class="category-header ${category}">
                        <div class="d-flex justify-content-between align-items-center">
                            <h6 class="mb-0">${getCategoryBadge(category)}</h6>
                            <span class="badge bg-light text-dark">${categoryCompleted}/${categoryTotal} (${categoryPercentage}%)</span>
                        </div>
                    </div>
                    ${categoryItems.map(item => `
                        <div class="checklist-item ${item.completed ? 'completed' : ''}">
                            <div class="checklist-item-header">
                                <p class="checklist-item-description ${item.completed ? 'text-completed' : 'text-pending'}">
                                    ${item.description}
                                </p>
                                <div>
                                    <button class="btn btn-sm ${item.completed ? 'btn-success' : 'btn-outline-success'} me-2"
                                            onclick="Checklist.toggleItem(${checklist.id}, ${item.id}, ${!item.completed})"
                                            title="${item.completed ? 'Marcar como pendiente' : 'Marcar como completado'}">
                                        <i class="bi ${item.completed ? 'bi-check-circle-fill' : 'bi-circle'}"></i>
                                    </button>
                                    ${!item.completed ? `
                                    <button class="btn btn-sm btn-outline-primary"
                                            onclick="Checklist.addNote(${checklist.id}, ${item.id})"
                                            title="Agregar nota">
                                        <i class="bi bi-chat"></i>
                                    </button>
                                    ` : ''}
                                </div>
                            </div>
                            ${item.notes ? `
                            <div class="checklist-item-notes">
                                <strong>Notas:</strong> ${item.notes}
                            </div>
                            ` : ''}
                        </div>
                    `).join('')}
                </div>
            `;
        });

        modalBody.innerHTML = `
            <div class="row mb-4">
                <div class="col-md-6">
                    <div class="checklist-detail-item">
                        <div class="checklist-detail-label">ID de Checklist</div>
                        <div class="checklist-detail-value">#${checklist.id}</div>
                    </div>
                    <div class="checklist-detail-item">
                        <div class="checklist-detail-label">Proyecto</div>
                        <div class="checklist-detail-value">${checklist.project_name}</div>
                    </div>
                    <div class="checklist-detail-item">
                        <div class="checklist-detail-label">Orden Asociada</div>
                        <div class="checklist-detail-value">#${checklist.order_id}</div>
                    </div>
                    <div class="checklist-detail-item">
                        <div class="checklist-detail-label">Supervisor</div>
                        <div class="checklist-detail-value">${checklist.supervisor}</div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="checklist-detail-item">
                        <div class="checklist-detail-label">Estado</div>
                        <div class="checklist-detail-value">${getStatusBadge(checklist.status)}</div>
                    </div>
                    <div class="checklist-detail-item">
                        <div class="checklist-detail-label">Programado para</div>
                        <div class="checklist-detail-value">${scheduledTime}</div>
                    </div>
                    <div class="checklist-detail-item">
                        <div class="checklist-detail-label">Creado el</div>
                        <div class="checklist-detail-value">${createdTime}</div>
                    </div>
                    <div class="checklist-detail-item">
                        <div class="checklist-detail-label">Completado el</div>
                        <div class="checklist-detail-value">${completedTime}</div>
                    </div>
                </div>
            </div>

            <div class="completion-stats">
                <h4>Progreso General</h4>
                <div class="progress mb-2" style="height: 20px;">
                    <div class="progress-bar bg-white" role="progressbar" 
                         style="width: ${progressPercentage}%">
                        <span class="progress-text text-dark">${progressPercentage}%</span>
                    </div>
                </div>
                <div class="d-flex justify-content-between text-white">
                    <span>${completedItems} de ${totalItems} items completados</span>
                    <span>${progressPercentage}%</span>
                </div>
            </div>

            <h5 class="mb-3">Items del Checklist</h5>
            ${itemsHTML}

            ${checklist.status !== 'completed' ? `
            <div class="text-center mt-4">
                <button class="btn btn-success btn-lg" onclick="Checklist.completeChecklist(${checklist.id})">
                    <i class="bi bi-check-circle me-2"></i>
                    Completar Checklist
                </button>
            </div>
            ` : ''}
        `;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('checklistModal'));
        modal.show();
    }

    function applyFilters() {
        const statusFilter = document.getElementById('status-filter').value;
        const categoryFilter = document.getElementById('category-filter').value;

        filteredChecklists = allChecklists.filter(checklist => {
            // Status filter
            if (statusFilter !== 'all' && checklist.status !== statusFilter) {
                return false;
            }
            
            // Category filter
            if (categoryFilter !== 'all') {
                const hasCategoryItem = checklist.items.some(item => item.category === categoryFilter);
                if (!hasCategoryItem) {
                    return false;
                }
            }
            
            return true;
        });

        displayChecklistsData(filteredChecklists);
    }

    // Public methods
    return {
        init: function() {
            document.addEventListener('DOMContentLoaded', function() {
                initChecklistPage();
            });
        },

        loadChecklistsSummary: async function() {
            try {
                const data = await apiCall('/api/v1/checklists-summary');
                document.getElementById('total-checklists').textContent = data.total_checklists;
                document.getElementById('todays-checklists').textContent = data.todays_checklists;
                document.getElementById('in-progress').textContent = data.in_progress;
                document.getElementById('completion-rate').textContent = data.completion_rate + '%';
                
                // Update progress bars
                document.getElementById('overall-progress').style.width = data.completion_rate + '%';
                document.getElementById('overall-progress').innerHTML = `<span class="progress-text">${data.completion_rate}%</span>`;
                document.getElementById('completed-items').textContent = data.completed_items + ' completados';
                document.getElementById('total-items').textContent = data.total_items + ' items total';
            } catch (error) {
                console.error('Error loading checklists summary:', error);
            }
        },

        loadChecklistsData: async function() {
            showLoading();
            try {
                const data = await apiCall('/api/checklists');
                allChecklists = data.data;
                filteredChecklists = [...allChecklists];
                displayChecklistsData(filteredChecklists);
            } catch (error) {
                console.error('Error loading checklists data:', error);
                showEmptyState();
            }
        },

        filterChecklists: function() {
            applyFilters();
        },

        clearFilters: function() {
            document.getElementById('status-filter').value = 'all';
            document.getElementById('category-filter').value = 'all';
            filteredChecklists = [...allChecklists];
            displayChecklistsData(filteredChecklists);
        },

        viewChecklistDetails: async function(checklistId) {
            try {
                const data = await apiCall(`/api/checklists/${checklistId}`);
                displayChecklistDetails(data.data);
            } catch (error) {
                console.error('Error loading checklist details:', error);
                showNotification('Error al cargar los detalles del checklist', 'error');
            }
        },

        showCreateModal: function() {
            const modal = new bootstrap.Modal(document.getElementById('createChecklistModal'));
            modal.show();
        },

        createChecklist: async function() {
            try {
                const categories = [];
                if (document.getElementById('category-pre').checked) categories.push('pre_vaciado');
                if (document.getElementById('category-seguridad').checked) categories.push('seguridad');
                if (document.getElementById('category-calidad').checked) categories.push('calidad');
                if (document.getElementById('category-post').checked) categories.push('post_vaciado');

                const formData = {
                    order_id: parseInt(document.getElementById('order-id').value),
                    project_name: document.getElementById('project-name').value,
                    supervisor: document.getElementById('supervisor').value,
                    scheduled_time: document.getElementById('scheduled-time').value,
                    categories: categories
                };

                // Basic validation
                if (!formData.order_id || !formData.project_name || !formData.supervisor || !formData.scheduled_time || categories.length === 0) {
                    showNotification('Por favor completa todos los campos requeridos', 'error');
                    return;
                }

                const data = await apiCall('/api/checklists', {
                    method: 'POST',
                    body: JSON.stringify(formData)
                });

                showNotification('Checklist creado exitosamente', 'success');
                
                // Close modal and refresh data
                const modal = bootstrap.Modal.getInstance(document.getElementById('createChecklistModal'));
                modal.hide();
                
                this.loadChecklistsSummary();
                this.loadChecklistsData();
                
            } catch (error) {
                console.error('Error creating checklist:', error);
                showNotification('Error al crear el checklist', 'error');
            }
        },

        toggleItem: async function(checklistId, itemId, completed) {
            try {
                const formData = new FormData();
                formData.append('completed', completed);

                await apiCall(`/api/checklists/${checklistId}/items/${itemId}`, {
                    method: 'PUT',
                    body: formData
                });

                showNotification('Item actualizado', 'success');
                this.loadChecklistsSummary();
                this.loadChecklistsData();
                
                // Refresh the modal if open
                const modal = document.getElementById('checklistModal');
                if (modal && modal.classList.contains('show')) {
                    this.viewChecklistDetails(checklistId);
                }
            } catch (error) {
                console.error('Error updating item:', error);
                showNotification('Error al actualizar el item', 'error');
            }
        },

        addNote: function(checklistId, itemId) {
            const note = prompt('Ingresa una nota para este item:');
            if (note) {
                // En una implementación real, aquí enviarías la nota al servidor
                showNotification('Función de notas en desarrollo', 'info');
            }
        },

        completeChecklist: async function(checklistId) {
            if (confirm('¿Estás seguro de que quieres marcar este checklist como completado?')) {
                try {
                    await apiCall(`/api/checklists/${checklistId}/complete`, {
                        method: 'PUT'
                    });

                    showNotification('Checklist completado exitosamente', 'success');
                    this.loadChecklistsSummary();
                    this.loadChecklistsData();
                    
                    // Close modal if open
                    const modal = bootstrap.Modal.getInstance(document.getElementById('checklistModal'));
                    if (modal) {
                        modal.hide();
                    }
                } catch (error) {
                    console.error('Error completing checklist:', error);
                    showNotification('Error al completar el checklist', 'error');
                }
            }
        },

        editChecklist: function(checklistId) {
            showNotification(`Función de edición para checklist ${checklistId} - En desarrollo`, 'info');
        }
    };
})();

// Auto-initialize
Checklist.init();