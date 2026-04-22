const API_URL = 'data.json';

async function updateDashboard() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        // Update Health Score
        const healthEl = document.getElementById('health-score');
        healthEl.innerText = data.health.score.toFixed(1);
        
        // Dynamic Border color based on score
        if (data.health.score > 85) healthEl.style.borderTopColor = 'var(--success)';
        else if (data.health.score > 50) healthEl.style.borderTopColor = 'var(--accent-color)';
        else healthEl.style.borderTopColor = 'var(--danger)';

        // Update Ledger
        const ledgerBody = document.getElementById('ledger-body');
        ledgerBody.innerHTML = data.ledger.map(entry => `
            <tr>
                <td style="color: var(--text-secondary)">${entry.timestamp.split('T')[0]} ${entry.timestamp.split('T')[1].slice(0,5)}</td>
                <td><strong>${entry.action.replace(/_/g, ' ')}</strong></td>
                <td><span class="hash">${entry.hash}</span></td>
                <td style="color: var(--success)">✅ Approved</td>
            </tr>
        `).join('');

        // Update Topology
        const topologyList = document.getElementById('topology-list');
        topologyList.innerHTML = data.topology.map(container => `
            <div style="margin-bottom: 1.5rem">
                <h4 style="color: var(--accent-color); margin-bottom: 0.5rem">${container.name}</h4>
                ${container.projects.map(p => `
                    <div style="display: flex; justify-content: space-between; padding: 0.5rem; background: rgba(255,255,255,0.03); border-radius: 4px; margin-bottom: 0.25rem">
                        <span>${p.name}</span>
                        <span style="color: var(--text-secondary); font-size: 0.75rem">${p.status}</span>
                    </div>
                `).join('')}
            </div>
        `).join('');

    } catch (error) {
        console.error('Error updating dashboard:', error);
    }
}

// Initial update and interval
updateDashboard();
setInterval(updateDashboard, 5000);
