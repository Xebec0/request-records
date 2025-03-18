// Global variables
let documentChart;
let requestTable;

// Analytics Chart Functions
function loadStats() {
    fetch(`/api/request-stats/?filter=${$('#timeFilter').val()}`)
        .then(response => response.json())
        .then(data => {
            updateDocumentChart(data.document_stats);
            updateProcessingTimes(data.processing_times);
        })
        .catch(error => {
            console.error('Error loading analytics data:', error);
        });
}

function updateDocumentChart(stats) {
    const ctx = document.getElementById('documentChart');
    
    if (documentChart) {
        documentChart.destroy();
    }
    
    // Create colors array based on the number of items
    const colors = generateChartColors(stats.length);
    
    documentChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: stats.map(s => s.request__document__description),
            datasets: [{
                data: stats.map(s => s.count),
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.formattedValue || '';
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((context.raw / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function updateProcessingTimes(times) {
    const container = document.getElementById('processingTimes');
    
    if (times.length === 0) {
        container.innerHTML = '<div class="alert alert-info">No processing data available for the selected time period.</div>';
        return;
    }
    
    container.innerHTML = times.map(t => `
        <div class="alert alert-${t.status === 'completed' ? 'success' : 'warning'} mb-2">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>Request #${t.request_id}</strong>: ${t.days} days, ${t.hours} hours
                </div>
                <span class="badge bg-${t.status === 'completed' ? 'success' : 'warning'}">
                    ${t.status}
                </span>
            </div>
        </div>
    `).join('');
}

// Helper function to generate nice chart colors
function generateChartColors(count) {
    const baseColors = [
        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
        '#6f42c1', '#fd7e14', '#20c9a6', '#5a5c69', '#858796'
    ];
    
    // If we have more items than colors, repeat colors with different opacity
    const colors = [];
    for (let i = 0; i < count; i++) {
        if (i < baseColors.length) {
            colors.push(baseColors[i]);
        } else {
            // Recycle colors with different opacity
            const colorIndex = i % baseColors.length;
            const opacity = 0.6 - (Math.floor(i / baseColors.length) * 0.2);
            colors.push(adjustColorOpacity(baseColors[colorIndex], opacity));
        }
    }
    
    return colors;
}

function adjustColorOpacity(hex, opacity) {
    // Convert hex to RGB
    let r = parseInt(hex.slice(1, 3), 16);
    let g = parseInt(hex.slice(3, 5), 16);
    let b = parseInt(hex.slice(5, 7), 16);
    
    // Return RGBA color
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
}

// Format status with appropriate styling
function formatStatus(cell) {
    const value = cell.getValue();
    let className = '';
    
    switch(value) {
        case 'Pending':
            className = 'status-pending';
            break;
        case 'Processing':
            className = 'status-processing';
            break;
        case 'Completed':
            className = 'status-completed';
            break;
        case 'Rejected':
            className = 'status-rejected';
            break;
        default:
            className = '';
    }
    
    return `<span class="${className}">${value}</span>`;
}

function initializeTable() {
    // Define column configuration with all columns visible by default
    const columns = [
        {title: "Ref. No.", field: "reference_number", headerHozAlign: "center", hozAlign: "center", width: 120, headerTooltip: true},
        {title: "Date Requested", field: "date_requested", headerHozAlign: "center", hozAlign: "center", sorter: "date", sorterParams: {format: "MMM DD, YYYY"}, width: 170, headerTooltip: true},
        {title: "Client Type", field: "client_type", headerHozAlign: "center", hozAlign: "center", width: 140, headerTooltip: true},
        {title: "Requested By", field: "requested_by", headerHozAlign: "center", width: 200, headerTooltip: true},
        {title: "Contact Details", field: "contact_details", headerHozAlign: "center", width: 160, headerTooltip: true},
        {title: "Email", field: "email", headerHozAlign: "center", width: 220, headerTooltip: true},
        {title: "Service Type", field: "service_type", headerHozAlign: "center", width: 200, headerTooltip: true},
        {title: "Purpose", field: "purpose", headerHozAlign: "center", width: 200, headerTooltip: true},
        {title: "Status", field: "status", headerHozAlign: "center", hozAlign: "center", formatter: formatStatus, width: 130, headerTooltip: true},
        {title: "Schedule", field: "schedule", headerHozAlign: "center", hozAlign: "center", width: 140, headerTooltip: true},
        {title: "Date Completed", field: "date_completed", headerHozAlign: "center", hozAlign: "center", width: 170, headerTooltip: true},
        {title: "Date Released", field: "date_released", headerHozAlign: "center", hozAlign: "center", width: 170, headerTooltip: true},
        {title: "Process Time", field: "processing_time", headerHozAlign: "center", hozAlign: "center", width: 160, headerTooltip: true}
    ];
    
    // Initialize Tabulator with horizontal scrolling and no column collapsing
    requestTable = new Tabulator("#requestTable", {
        ajaxURL: "/api/request-details/",
        ajaxResponse: function(url, params, response) {
            return response;
        },
        layout: "fitData",  // Fit columns to their data
        layoutColumnsOnNewData: true,
        columns: columns,
        initialSort: [{column: "date_requested", dir: "desc"}],
        height: "auto",
        maxHeight: "70vh",
        pagination: true,
        paginationSize: 15,
        paginationSizeSelector: [10, 15, 25, 50, 100, true],
        movableColumns: true,
        printAsHtml: true,
        printHeader: "<h3>Request Records</h3>",
        printFooter: "<p>Printed on " + new Date().toLocaleString() + "</p>",
        placeholder: "No Data Available",
        responsiveLayout: false,  // Disable responsive layout
        headerFilterPlaceholder: "Filter...",
        persistenceMode: "local",
        persistence: true,
        persistenceID: "requestTableState",
    });
    
    return requestTable;
}

// Date range filtering
function setupDateRangeFiltering(table) {
    $('#applyDateFilter').on('click', function() {
        const fromDate = $('#dateFrom').val();
        const toDate = $('#dateTo').val();
        
        if (fromDate || toDate) {
            // Apply the filter when both dates are selected
            table.setFilter(function(data) {
                if (!data.date_requested) return true;
                
                // Convert the date string to Date object for comparison (format: "MMM DD, YYYY")
                const dateParts = data.date_requested.split(' ');
                const month = dateParts[0];
                const day = parseInt(dateParts[1].replace(',', ''));
                const year = parseInt(dateParts[2]);
                
                const months = {
                    'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 
                    'May': 4, 'Jun': 5, 'Jul': 6, 'Aug': 7,
                    'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
                };
                
                const rowDate = new Date(year, months[month], day);
                
                let valid = true;
                if (fromDate && !isNaN(new Date(fromDate))) {
                    valid = valid && rowDate >= new Date(fromDate);
                }
                
                if (toDate && !isNaN(new Date(toDate))) {
                    valid = valid && rowDate <= new Date(toDate);
                }
                
                return valid;
            });
        }
    });
    
    $('#clearDateFilter').on('click', function() {
        $('#dateFrom, #dateTo').val('');
        table.clearFilter();
    });
}


// Set up export functionality
function setupExportButtons(table) {
    // Export to CSV
    document.getElementById("export-csv").addEventListener("click", function() {
        table.download("csv", "reports_summaary.csv", {
            sheetName: "Reports Summary"
        });
    });
    
    // Export to Excel
    document.getElementById("export-excel").addEventListener("click", function() {
        table.download("xlsx", "reports_summaary.xlsx", {
            sheetName: "Reports Summary"
        });
    });
    
    // Export to PDF with smaller fonts and bold title
    document.getElementById("export-pdf").addEventListener("click", function() {
        table.download("pdf", "reports_summary.pdf", {
            orientation: "landscape",
            title: "Reports Summary",
            autoTable: {
                styles: {
                    headerColor: [41, 128, 185],
                    fontStyle: 'bold',
                    fontSize: 7,
                    cellPadding: 3
                },
                headStyles: {
                    fontSize: 8,
                    fontStyle: 'bold',
                    halign: 'center'
                },
                columnStyles: {
                    id: {fontStyle: 'bold'}
                },
                margin: {top: 45, left: 10, right: 10},
                didDrawPage: function(data) {
                    let doc = data.doc;
                    doc.setFontSize(14);
                    doc.setFont(undefined, 'bold');
                    doc.text("Request Records", data.settings.margin.left, 20);
                    
                    doc.setFontSize(10);
                    doc.setFont(undefined, 'normal');
                    doc.text("Generated on: " + new Date().toLocaleString(), data.settings.margin.left, 25);
                }
            }
        });
    });
    
}

// Handle tab switching (ensure table is correctly sized when tab becomes visible)
function setupTabSwitching(table) {
    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        if (e.target.id === 'request-data-tab') {
            table.redraw(true); // Force a full redraw of the table
        } else if (e.target.id === 'charts-tab') {
            loadStats(); // Load chart data when switching to charts tab
        }
    });
}

// Setup global search functionality
function setupSearchFunctionality(table) {
    // Search as you type with debounce
    let searchTimeout;
    $('#searchInput').on('input', function() {
        const searchValue = $(this).val();
        
        // Clear any pending timeouts to avoid multiple rapid searches
        clearTimeout(searchTimeout);
        
        // Set a short timeout to avoid searching on every keystroke
        searchTimeout = setTimeout(function() {
            if (searchValue === '') {
                table.clearFilter();
            } else {
                performSearch(table, searchValue);
            }
        }, 300); // 300ms delay for smoother typing experience
    });
    
    // Keep the button click handler as an alternative
    $('#searchButton').on('click', function() {
        const searchValue = $('#searchInput').val();
        performSearch(table, searchValue);
    });
    
    // Keep the Enter key handler for compatibility
    $('#searchInput').on('keyup', function(e) {
        if (e.key === 'Enter') {
            const searchValue = $(this).val();
            performSearch(table, searchValue);
        }
    });
}

// Perform the actual search across all columns
function performSearch(table, value) {
    if (value === '') {
        table.clearFilter();
        return;
    }
    
    // Apply filter to search across all fields
    table.setFilter(function(data) {
        // Search in all object properties
        for (let key in data) {
            // Skip if property doesn't exist or is null
            if (!data[key]) continue;
            
            // Convert both to lowercase for case-insensitive search
            if (String(data[key]).toLowerCase().includes(value.toLowerCase())) {
                return true;
            }
        }
        return false;
    });
}

// Then, in the document ready function, add:
$(document).ready(function() {
    // Load charts data
    $('#timeFilter').change(loadStats);
    loadStats();
    
    // Initialize and setup Tabulator table
    const table = initializeTable();
    setupDateRangeFiltering(table);
    setupExportButtons(table);
    setupSearchFunctionality(table); // Add this line
    setupTabSwitching(table);
    
    // Handle window resize
    $(window).resize(function() {
        if (table) {
            table.redraw(true);
        }
    });
});
