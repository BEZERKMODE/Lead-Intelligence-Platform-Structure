/* ==========================================================================
   Lead Intelligence Platform - Premium Javascript Engine
   ========================================================================== */

let leadsList = [];
let selectedLead = null;
let mapInstance = null;
let mapMarkers = [];
let activeTab = 'dashboard';

// On Document Ready
document.addEventListener("DOMContentLoaded", () => {
    initMap();
    fetchLeads();
    fetchAnalytics();
    
    // Auto refresh analytics every 30 seconds
    setInterval(fetchAnalytics, 30000);
});

// Initialize Leaflet Map
function initMap() {
    // Standard Dark Matter tiles coordinate setup
    mapInstance = L.map('leads-map', {
        zoomControl: true,
        maxZoom: 18,
        minZoom: 1
    }).setView([30.0, 0.0], 2); // Global world view center
    
    // Sleek cartographic Dark Mode tile template
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(mapInstance);
    
    // Delay slightly to fix Leaflet size rendering bug
    setTimeout(() => {
        mapInstance.invalidateSize();
    }, 400);
}

// Fetch Leads list with current filter and search
function fetchLeads() {
    const search = document.getElementById('lead-search').value;
    const sector = document.getElementById('filter-sector').value;
    const status = document.getElementById('filter-status').value;
    
    let url = `/api/leads?search=${encodeURIComponent(search)}&sector=${encodeURIComponent(sector)}&status=${encodeURIComponent(status)}`;
    
    fetch(url)
        .then(res => res.json())
        .then(leads => {
            leadsList = leads;
            renderLeadsTable(leads);
            updateLeadsMap(leads);
        })
        .catch(err => {
            console.error("Failed to fetch leads", err);
            showToast("Failed to reload directory", "error");
        });
}

// Fetch general system metrics
function fetchAnalytics() {
    fetch('/api/analytics')
        .then(res => res.json())
        .then(data => {
            document.getElementById('metric-total').innerText = data.metrics.total_leads;
            document.getElementById('metric-qualified').innerText = data.metrics.highly_qualified;
            document.getElementById('metric-match').innerText = `${data.metrics.avg_priority_score}%`;
            document.getElementById('metric-crm').innerText = data.metrics.synced_crm_count;
        })
        .catch(err => console.error("Failed to fetch analytics", err));
}

// Update Map Pin coordinates
function updateLeadsMap(leads) {
    // Clear old markers
    mapMarkers.forEach(m => mapInstance.removeLayer(m));
    mapMarkers = [];
    
    const validLeads = leads.filter(l => l.latitude !== 0.0 && l.longitude !== 0.0);
    
    if (validLeads.length === 0) return;
    
    validLeads.forEach(lead => {
        // Build Custom Glowing Pin DivIcon
        let markerColor = 'var(--accent)';
        if (lead.status === 'SQL') markerColor = 'var(--color-sql)';
        if (lead.status === 'Contacted') markerColor = 'var(--color-contacted)';
        if (lead.status === 'New') markerColor = 'var(--color-new)';
        
        const customIcon = L.divIcon({
            html: `<div style="background-color: ${markerColor}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 10px ${markerColor};"></div>`,
            className: 'custom-map-pin',
            iconSize: [12, 12]
        });
        
        const marker = L.marker([lead.latitude, lead.longitude], { icon: customIcon })
            .addTo(mapInstance)
            .bindPopup(`
                <div style="font-family: var(--font-sans); color: #000; padding: 4px;">
                    <strong style="font-size: 14px;">${lead.company_name}</strong><br>
                    <span style="font-size: 12px; color: #555;">${lead.sector}</span><br>
                    <span style="font-size: 11px; font-weight: bold; color: var(--accent);">Score: ${lead.priority_score}/100</span><br>
                    <button onclick="openLeadDrawer(${lead.id})" style="margin-top: 6px; padding: 4px 8px; font-size: 11px; background: #000; color: #fff; border: none; border-radius: 4px; cursor: pointer;">Open Profile</button>
                </div>
            `);
            
        mapMarkers.push(marker);
    });
    
    // Automatically fit map view boundary to fit coordinates nicely
    if (validLeads.length > 0) {
        const group = new L.featureGroup(mapMarkers);
        mapInstance.fitBounds(group.getBounds().pad(0.15));
    }
}

// Render leads rows dynamically
function renderLeadsTable(leads) {
    const list = document.getElementById('leads-list');
    list.innerHTML = '';
    
    if (leads.length === 0) {
        list.innerHTML = `
            <tr>
                <td colspan="7" style="text-align: center; color: var(--text-secondary); padding: 40px;">
                    <i class="fa-solid fa-users-slash" style="font-size: 24px; margin-bottom: 8px; display: block;"></i>
                    No leads found matching your search.
                </td>
            </tr>
        `;
        return;
    }
    
    leads.forEach(lead => {
        const statusClass = `badge-${lead.status.toLowerCase()}`;
        const scoreClass = lead.priority_score >= 80 ? 'priority-high' : (lead.priority_score >= 50 ? 'priority-mid' : 'priority-low');
        
        // Render tech pills up to 3
        const techList = lead.technologies || [];
        const techHTML = techList.slice(0, 3).map(t => `<span class="tech-pill">${t}</span>`).join('') +
                         (techList.length > 3 ? `<span class="tech-pill">+${techList.length - 3}</span>` : '');
                         
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>
                <div class="company-cell">
                    <span class="company-title">${lead.company_name}</span>
                    <a href="https://${lead.domain}" target="_blank" class="company-domain">${lead.domain}</a>
                </div>
            </td>
            <td>${lead.sector}</td>
            <td><i class="fa-solid fa-location-dot" style="color: var(--text-secondary); margin-right: 4px;"></i> ${lead.location}</td>
            <td>
                <div class="priority-meter ${scoreClass}">
                    ${lead.priority_score || '—'}
                </div>
            </td>
            <td>
                <div class="tech-pills">${techHTML || '<span style="color: var(--text-muted);">None</span>'}</div>
            </td>
            <td><span class="badge ${statusClass}">${lead.status}</span></td>
            <td>
                <div class="action-icons">
                    <button class="action-icon-btn" onclick="openLeadDrawer(${lead.id})" title="View Details">
                        <i class="fa-solid fa-folder-open"></i>
                    </button>
                    <button class="action-icon-btn" onclick="syncLeadCRMDirect(${lead.id})" title="Push to CRM">
                        <i class="fa-solid fa-cloud-arrow-up"></i>
                    </button>
                    <button class="action-icon-btn" onclick="deleteLead(${lead.id})" title="Remove Lead" style="color: var(--text-muted);">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            </td>
        `;
        list.appendChild(tr);
    });
}

// Tab switcher navigation handler
function switchTab(tabName) {
    activeTab = tabName;
    
    // Update nav classes
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    document.getElementById(`nav-${tabName}`).classList.add('active');
    
    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');
    const visSection = document.getElementById('vis-section');
    
    if (tabName === 'dashboard') {
        pageTitle.innerText = "Sales Analytics Dashboard";
        pageSubtitle.innerText = "Real-time target account intelligence & automated outreach profiling";
        visSection.style.display = 'grid';
        fetchLeads();
        setTimeout(() => mapInstance.invalidateSize(), 300);
    } else if (tabName === 'leads') {
        pageTitle.innerText = "Lead Directory Cabinet";
        pageSubtitle.innerText = "Filter, search, review, and manage synced CRM records";
        visSection.style.display = 'none'; // Hide map/console for directory focus
        fetchLeads();
    } else if (tabName === 'scraper') {
        pageTitle.innerText = "AI Web Scraper Engine";
        pageSubtitle.innerText = "Execute real-time technology stack crawling and email harvesting";
        visSection.style.display = 'grid';
        // Scroll directly to Console and focus crawl input
        document.getElementById('crawl-domain').focus();
    }
}

// Server Sent Events (SSE) log terminal trigger
function triggerConsoleScrape() {
    const domainInput = document.getElementById('crawl-domain');
    const domain = domainInput.value.trim();
    
    if (!domain) {
        showToast("Please enter a domain website first", "error");
        return;
    }
    
    const consoleOut = document.getElementById('console-output');
    consoleOut.innerHTML = `<span class="log-start">⚡ Kicking off real-time scraper for: ${domain}...</span>`;
    
    // Disable inputs during scrape
    domainInput.disabled = true;
    
    // Connect to Server event stream
    const source = new EventSource(`/api/leads/scrape-stream?domain=${encodeURIComponent(domain)}`);
    
    source.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        if (data.error) {
            consoleOut.innerHTML += `<br><span class="log-error">❌ Scrape error: ${data.error}</span>`;
            source.close();
            domainInput.disabled = false;
            showToast("Scraper halted on error", "error");
            return;
        }
        
        if (data.log) {
            const catClass = `log-${data.category}`;
            consoleOut.innerHTML += `<br><span class="${catClass}">[Scraper]: ${data.log}</span>`;
            consoleOut.scrollTop = consoleOut.scrollHeight; // Auto scroll
        }
        
        if (data.complete) {
            source.close();
            domainInput.disabled = false;
            domainInput.value = '';
            
            // Reload leads list and dashboard values
            fetchLeads();
            fetchAnalytics();
            
            showToast(`Scraped & enriched profile for: ${domain}`, "success");
            
            // Automatically pop open Drawer cabinet for the newly scraped lead
            setTimeout(() => {
                openLeadDrawer(data.lead_id);
            }, 600);
        }
    };
    
    source.onerror = function() {
        consoleOut.innerHTML += `<br><span class="log-error">❌ SSE connection failure. Halting engine.</span>`;
        source.close();
        domainInput.disabled = false;
    };
}

// Sidebar Drawer operations
function openLeadDrawer(leadId) {
    fetch(`/api/leads/${leadId}`)
        .then(res => res.json())
        .then(lead => {
            selectedLead = lead;
            
            // Fill details
            document.getElementById('drawer-company-name').innerText = lead.company_name;
            document.getElementById('drawer-domain').innerText = lead.domain;
            document.getElementById('drawer-domain').href = `https://${lead.domain}`;
            document.getElementById('drawer-priority').innerText = `${lead.priority_score || 0}/100`;
            document.getElementById('drawer-match-rate').innerText = `${lead.ai_match_rate || 0}%`;
            document.getElementById('drawer-growth').innerText = lead.growth_trend;
            document.getElementById('drawer-employees').innerText = lead.employees;
            document.getElementById('drawer-revenue').innerText = lead.revenue;
            const latVal = (lead.latitude !== null && lead.latitude !== undefined) ? Number(lead.latitude).toFixed(4) : '0.0000';
            const lngVal = (lead.longitude !== null && lead.longitude !== undefined) ? Number(lead.longitude).toFixed(4) : '0.0000';
            document.getElementById('drawer-coords').innerText = `${latVal}, ${lngVal}`;
            document.getElementById('drawer-phone').innerText = lead.phone || 'Not Available';
            
            // Render Tech pills
            const pillsBox = document.getElementById('drawer-tech-pills');
            pillsBox.innerHTML = '';
            if (lead.technologies && lead.technologies.length > 0) {
                lead.technologies.forEach(t => {
                    const pill = document.createElement('span');
                    pill.className = 'tech-pill';
                    pill.style.padding = '4px 10px';
                    pill.style.fontSize = '12px';
                    pill.innerText = t;
                    pillsBox.appendChild(pill);
                });
            } else {
                pillsBox.innerHTML = '<span style="color: var(--text-muted); font-size: 13px;">No technologies recorded.</span>';
            }
            
            // Contacts and notes
            document.getElementById('drawer-contacts').innerText = lead.contacts || 'No verified contacts harvested.';
            document.getElementById('drawer-notes-input').value = lead.notes || '';
            
            // Cybersecurity Perimeter Data
            const secScoreEl = document.getElementById('drawer-security-score');
            const scoreGrade = lead.security_score || 'A';
            secScoreEl.innerText = scoreGrade;
            
            // Color grade accordingly
            secScoreEl.className = 'priority-meter';
            if (scoreGrade === 'A') {
                secScoreEl.style.backgroundColor = 'var(--accent)'; // Emerald
                secScoreEl.style.color = '#fff';
            } else if (scoreGrade === 'B') {
                secScoreEl.style.backgroundColor = 'var(--color-new)'; // Teal
                secScoreEl.style.color = '#fff';
            } else if (scoreGrade === 'C') {
                secScoreEl.style.backgroundColor = 'var(--color-contacted)'; // Orange/Amber
                secScoreEl.style.color = '#fff';
            } else {
                secScoreEl.style.backgroundColor = 'var(--color-lost)'; // Red
                secScoreEl.style.color = '#fff';
            }
            
            // Render Mapped Subdomains
            const subdomainsBox = document.getElementById('drawer-subdomains');
            subdomainsBox.innerHTML = '';
            const subdomainList = lead.subdomains || [];
            if (subdomainList.length > 0) {
                subdomainList.forEach(sub => {
                    const pill = document.createElement('span');
                    pill.className = 'tech-pill';
                    pill.style.padding = '2px 8px';
                    pill.style.fontSize = '11px';
                    pill.style.backgroundColor = 'var(--bg-main)';
                    pill.style.border = '1px solid var(--border-color)';
                    pill.innerText = sub;
                    subdomainsBox.appendChild(pill);
                });
            } else {
                subdomainsBox.innerHTML = '<span style="color: var(--text-muted); font-size: 12px;">No subdomains mapped yet.</span>';
            }
            
            // Render Vulnerabilities
            const vulnsBox = document.getElementById('drawer-vulnerabilities');
            vulnsBox.innerHTML = '';
            const vulnsList = lead.vulnerabilities || [];
            if (vulnsList.length > 0 && vulnsList[0] !== '') {
                vulnsList.forEach(vuln => {
                    const li = document.createElement('li');
                    li.style.fontSize = '12px';
                    li.style.color = 'var(--text-secondary)';
                    li.style.display = 'flex';
                    li.style.alignItems = 'center';
                    li.innerHTML = `<i class="fa-solid fa-circle-exclamation" style="color: ${scoreGrade === 'A' ? 'var(--accent)' : 'var(--color-lost)'}; margin-right: 8px;"></i> <span>${vuln}</span>`;
                    vulnsBox.appendChild(li);
                });
            } else {
                vulnsBox.innerHTML = '<li style="font-size: 12px; color: var(--accent);"><i class="fa-solid fa-circle-check" style="margin-right: 8px;"></i> Zero critical external exposures detected.</li>';
            }
            
            // Clear or fetch email Outreach
            document.getElementById('drawer-email').innerText = "Click 'Rewrite Copy' above to synthesize a personalized AI outreach email...";
            
            // Open Cabinet drawer
            document.getElementById('detailDrawer').classList.add('open');
        })
        .catch(err => {
            console.error("Failed to fetch lead details", err);
            showToast("Failed to open drawer details", "error");
        });
}

function closeDrawer() {
    document.getElementById('detailDrawer').classList.remove('open');
    selectedLead = null;
}

// Generate Personalized Outreach email via AI
function triggerEmailGeneration() {
    if (!selectedLead) return;
    
    const emailBox = document.getElementById('drawer-email');
    emailBox.innerText = "🤖 Invoking ML outreach copywriter...";
    
    fetch(`/api/leads/${selectedLead.id}/email`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            emailBox.innerText = data.email;
            showToast("AI Outreach synthesized!", "success");
        })
        .catch(err => {
            console.error("Failed to generate outreach", err);
            emailBox.innerText = "❌ Outreach copywriting model failed to generate template.";
        });
}

// Copy Outreach to Clipboard
function copyOutreachEmail() {
    const emailText = document.getElementById('drawer-email').innerText;
    if (emailText.includes("synthesize a personalized") || emailText.includes("Invoking ML")) {
        showToast("Generate an outreach email first!", "error");
        return;
    }
    
    navigator.clipboard.writeText(emailText)
        .then(() => showToast("Copied outreach to clipboard!", "success"))
        .catch(() => showToast("Failed to copy clipboard", "error"));
}

// Push to CRM Salesforce or HubSpot
function syncLeadCRM(crmName) {
    if (!selectedLead) return;
    
    showToast(`Initiating data push to ${crmName}...`, "info");
    
    fetch(`/api/leads/${selectedLead.id}/sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ crm: crmName })
    })
    .then(res => res.json())
    .then(data => {
        showToast(`Synced! Record created: ${data.crm_record_id}`, "success");
        closeDrawer();
        fetchLeads();
        fetchAnalytics();
    })
    .catch(err => {
        console.error("Sync error", err);
        showToast("Integration payload error", "error");
    });
}

function syncLeadCRMDirect(leadId) {
    showToast("Triggering cloud CRM integration...", "info");
    fetch(`/api/leads/${leadId}/sync`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ crm: 'Salesforce' })
    })
    .then(res => res.json())
    .then(data => {
        showToast(`Salesforce Sync: ${data.crm_record_id}`, "success");
        fetchLeads();
        fetchAnalytics();
    })
    .catch(err => showToast("CRM push failed", "error"));
}

// Save Private Notes inside Drawer
function saveDrawerNotes() {
    if (!selectedLead) return;
    
    const notes = document.getElementById('drawer-notes-input').value;
    
    fetch(`/api/leads/${selectedLead.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes: notes })
    })
    .then(res => res.json())
    .then(data => {
        selectedLead.notes = notes;
        showToast("Lead notes saved", "success");
    })
    .catch(err => showToast("Failed to save notes", "error"));
}

// Create new lead manually
function submitNewLead(event) {
    event.preventDefault();
    
    const domain = document.getElementById('add-domain').value.trim();
    const companyName = document.getElementById('add-company').value.trim();
    const sector = document.getElementById('add-sector').value;
    const location = document.getElementById('add-location').value.trim();
    
    fetch('/api/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            domain: domain,
            company_name: companyName,
            sector: sector,
            location: location
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, "error");
        } else {
            showToast("Lead account recorded!", "success");
            closeModal('addLeadModal');
            document.getElementById('add-lead-form').reset();
            fetchLeads();
            fetchAnalytics();
        }
    })
    .catch(err => showToast("Failed to record lead", "error"));
}

// Bulk CSV loader Form submission
function submitCSVImport(event) {
    event.preventDefault();
    
    const fileField = document.getElementById('csv-file');
    if (fileField.files.length === 0) return;
    
    const formData = new FormData();
    formData.append('file', fileField.files[0]);
    
    showToast("Reading and uploading CSV...", "info");
    
    fetch('/api/leads/import', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            showToast(data.error, "error");
        } else {
            showToast(`Bulk Sync Complete. Imported ${data.imported_count} accounts!`, "success");
            closeModal('importModal');
            document.getElementById('import-csv-form').reset();
            fetchLeads();
            fetchAnalytics();
        }
    })
    .catch(err => showToast("Bulk import failed", "error"));
}

// Delete Lead from Local DB
function deleteLead(leadId) {
    if (!confirm("Are you sure you want to remove this lead profile?")) return;
    
    fetch(`/api/leads/${leadId}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(() => {
            showToast("Lead removed from database", "success");
            fetchLeads();
            fetchAnalytics();
        })
        .catch(err => showToast("Deletion failed", "error"));
}

// Modal Toggle utilities
function openModal(id) {
    document.getElementById(id).classList.add('open');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('open');
}

// Beautiful Custom Toast Notification Systems
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    
    let iconHTML = '<i class="fa-solid fa-circle-check" style="color: var(--accent);"></i>';
    if (type === 'error') {
        toast.style.borderLeftColor = 'var(--color-lost)';
        iconHTML = '<i class="fa-solid fa-circle-exclamation" style="color: var(--color-lost);"></i>';
    } else if (type === 'info') {
        toast.style.borderLeftColor = 'var(--color-new)';
        iconHTML = '<i class="fa-solid fa-circle-info" style="color: var(--color-new);"></i>';
    }
    
    toast.innerHTML = `${iconHTML} <span>${message}</span>`;
    container.appendChild(toast);
    
    // Smoothly fade out and delete
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-10px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Copy Full Cybersecurity Perimeter Assessment Report (Suraj's Pre-Sales Power Tool!)
function copyFullPerimeterReport() {
    if (!selectedLead) return;
    
    const emailText = document.getElementById('drawer-email').innerText;
    const subdomains = selectedLead.subdomains ? selectedLead.subdomains.join(', ') : 'None mapped';
    const vulnerabilities = selectedLead.vulnerabilities ? selectedLead.vulnerabilities.join('\n- ') : 'No critical exposures';
    
    const reportMarkdown = `
# KINSTECHNOLOGY CYBERSECURITY PERIMETER ASSESSMENT REPORT
======================================================================
TARGET ACCOUNT: ${selectedLead.company_name} (${selectedLead.domain})
HQ Location:    ${selectedLead.location}
Market Sector:  ${selectedLead.sector}
Estimated Size: ${selectedLead.employees}

----------------------------------------------------------------------
🛡️ PERIMETER HYGIENE ASSESSMENT
----------------------------------------------------------------------
KinsTechnology Security Grade: [ ${selectedLead.security_score || 'A'} ]

Mapped Active Subdomains:
${subdomains}

Detected Exposure Points / Vulnerabilities:
- ${vulnerabilities}

----------------------------------------------------------------------
✉️ PRE-SALES OUTREACH DRAFT (Prepared by Suraj Singh Bartwal)
----------------------------------------------------------------------
${emailText.includes("synthesize a personalized") ? "(No custom email generated yet. Run AI Rewrite Copy to bundle output)" : emailText}
======================================================================
Generated via LeadIntel Platform v2 • KinsTechnology Pre-Sales Suite
`;

    navigator.clipboard.writeText(reportMarkdown.trim())
        .then(() => showToast("Copied full visual security report!", "success"))
        .catch(() => showToast("Failed to copy report", "error"));
}
