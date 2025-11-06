// Home Page JavaScript Module - Concrete Pouring System
const Home = (function() {
    // Private variables
    let dataContainer;
    let scheduleContainer;
    let actionButtons;

    // Private methods
    function initHomePage() {
        dataContainer = document.getElementById('data-container');
        scheduleContainer = document.getElementById('schedule-container');
        actionButtons = document.querySelectorAll('.action-btn');
        
        initializeActionButtons();
        initializeCardAnimations();
    }

    function initializeActionButtons() {
        actionButtons.forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }

    function initializeCardAnimations() {
        const statCards = document.querySelectorAll('.stat-card');
        statCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            card.classList.add('slide-up');
        });
    }

    function displaySchedule(schedule) {
        if (!scheduleContainer) return;
        
        if (schedule.length === 0) {
            scheduleContainer.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-calendar-x display-4 d-block mb-2"></i>
                    <p class="mb-0">No hay programaciones para hoy</p>
                </div>
            `;
            return;
        }

        let scheduleHTML = '<div class="table-responsive"><table class="table table-hover">';
        scheduleHTML += `
            <thead>
                <tr>
                    <th>Hora</th>
                    <th>Proyecto</th>
                    <th>Cliente</th>
                    <th>Mezcla</th>
                    <th>Volumen (m³)</th>
                    <th>Estado</th>
                </tr>
            </thead>
            <tbody>
        `;

        schedule.forEach(item => {
            const statusBadge = getStatusBadge(item.status);
            scheduleHTML += `
                <tr>
                    <td><strong>${item.scheduled_time}</strong></td>
                    <td>${item.project_name}</td>
                    <td>${item.client}</td>
                    <td><span class="badge bg-secondary">${item.mix_type}</span></td>
                    <td>${item.volume}</td>
                    <td>${statusBadge}</td>
                </tr>
            `;
        });

        scheduleHTML += '</tbody></table></div>';
        scheduleContainer.innerHTML = scheduleHTML;
    }

    function getStatusBadge(status) {
        const statusMap = {
            'scheduled': 'bg-primary',
            'preparing': 'bg-warning',
            'in_progress': 'bg-info',
            'completed': 'bg-success',
            'cancelled': 'bg-danger'
        };
        
        const statusText = {
            'scheduled': 'Programado',
            'preparing': 'Preparando',
            'in_progress': 'En Progreso',
            'completed': 'Completado',
            'cancelled': 'Cancelado'
        };
        
        return `<span class="badge ${statusMap[status] || 'bg-secondary'}">${statusText[status] || status}</span>`;
    }

    function showLoading(message) {
        if (!dataContainer) return;
        
        dataContainer.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="text-muted mb-0">${message}</p>
            </div>
        `;
    }

    function showError(message) {
        if (!dataContainer) return;
        
        dataContainer.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
    }

    function displayData(data, message) {
        if (!dataContainer) return;
        
        dataContainer.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
            <pre class="bg-dark text-light p-3 rounded mb-0"><code>${JSON.stringify(data, null, 2)}</code></pre>
        `;
    }

    // Public methods
    return {
        init: function() {
            document.addEventListener('DOMContentLoaded', function() {
                initHomePage();
            });
        },

        loadSchedule: async function() {
            showLoading('Cargando programación...');
            try {
                const data = await apiCall('/api/v1/schedule');
                displaySchedule(data);
                // Clear data container after loading schedule
                this.clearData();
            } catch (error) {
                showError('Error cargando programación: ' + error.message);
            }
        },

        loadProjects: async function() {
            showLoading('Cargando proyectos...');
            try {
                const data = await apiCall('/api/v1/projects');
                displayData(data, 'Proyectos cargados exitosamente');
            } catch (error) {
                showError('Error cargando proyectos: ' + error.message);
            }
        },

        loadMixes: async function() {
            showLoading('Cargando mezclas de concreto...');
            try {
                const data = await apiCall('/api/v1/concrete-mixes');
                displayData(data, 'Mezclas cargadas exitosamente');
            } catch (error) {
                showError('Error cargando mezclas: ' + error.message);
            }
        },

        loadStats: async function() {
            showLoading('Cargando estadísticas...');
            try {
                const data = await apiCall('/api/v1/concrete-stats');
                displayData(data, 'Estadísticas cargadas exitosamente');
            } catch (error) {
                showError('Error cargando estadísticas: ' + error.message);
            }
        },

        clearData: function() {
            if (!dataContainer) return;
            
            dataContainer.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-cone-striped display-4 d-block mb-2"></i>
                    <p class="mb-0">Selecciona una acción para cargar datos</p>
                </div>
            `;
        }
    };
})();

// Auto-initialize
Home.init();